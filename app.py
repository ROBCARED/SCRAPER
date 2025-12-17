import streamlit as st
import pandas as pd

st.title("Exploration des jobs — Top 10 KPI")

# Charger le CSV Top10
try:
	df = pd.read_csv("kpi_tasks_ratio_top10.csv", sep=';')
except FileNotFoundError:
	st.error("Fichier 'kpi_tasks_ratio_top10.csv' introuvable. Exécutez d'abord le pipeline.")
	st.stop()

# Normaliser noms de colonnes (tolérance majuscules/minuscules)
cols = {c.lower(): c for c in df.columns}
def col(name):
	return cols.get(name.lower())

poste_col = col('poste')
entreprise_col = col('entreprise')
liste_col = col('liste_taches') or col('liste_taches')
complex_col = col('complexite') or col('complexite')
salaire_col = col('salaire_annuel_estime') or col('salaire')
ratio_col = col('ratio_taches_par_salaire') or col('ratio_taches_par_salaire')
link_col = col('lien')

# Construire colonnes d'affichage
display_df = pd.DataFrame()
display_df['Poste'] = df[poste_col] if poste_col in df else df.get(poste_col, '')
display_df['Entreprise'] = df[entreprise_col] if entreprise_col in df else df.get(entreprise_col, '')

# Liste des tâches : nettoyer la représentation si c'est une string
def parse_list_cell(x):
	if isinstance(x, list):
		return x
	s = str(x)
	if s.startswith('[') and s.endswith(']'):
		# retirer crochets et quotes
		inner = s[1:-1].strip()
		if not inner:
			return []
		parts = [p.strip().strip("'\"") for p in inner.split(',')]
		return parts
	return [s] if s and s != 'nan' else []

if liste_col in df:
	display_df['Liste_taches'] = df[liste_col].apply(parse_list_cell)
else:
	display_df['Liste_taches'] = [[] for _ in range(len(df))]

# Complexité numérique
if complex_col in df:
	display_df['Complexite'] = pd.to_numeric(df[complex_col], errors='coerce').fillna(0).astype(int)
else:
	display_df['Complexite'] = display_df['Liste_taches'].apply(len)

# Salaire et ratio
display_df['Salaire_annuel_estime'] = pd.to_numeric(df[salaire_col], errors='coerce') if salaire_col in df else pd.NA
display_df['Ratio_Taches_par_Salaire'] = pd.to_numeric(df[ratio_col], errors='coerce') if ratio_col in df else pd.NA

# Lien cliquable
if link_col in df:
	display_df['Lien'] = df[link_col]
else:
	display_df['Lien'] = ''

# Normaliser colonne salaire numérique pour filtrage
display_df['Salaire_annuel_estime'] = pd.to_numeric(display_df['Salaire_annuel_estime'], errors='coerce')

# Filtre salaire dans la sidebar (range)
if display_df['Salaire_annuel_estime'].notna().any():
	min_sal = int(display_df['Salaire_annuel_estime'].min(skipna=True))
	max_sal = int(display_df['Salaire_annuel_estime'].max(skipna=True))
	default_min = min_sal
	default_max = max_sal
else:
	min_sal, max_sal = 0, 200000
	default_min, default_max = min_sal, min(50000, max_sal)

sal_range = st.sidebar.slider("Salaire annuel (€)", min_sal, max(200000, max_sal), (default_min, default_max))
sel_min, sel_max = sal_range

# Appliquer filtre salaire
filtered_df = display_df[(display_df['Salaire_annuel_estime'].fillna(0) >= sel_min) & (display_df['Salaire_annuel_estime'].fillna(0) <= sel_max)]

# Vue : choix entre Tableau / Détails / Graphiques
view = st.sidebar.radio("Vue", ("Tableau", "Détails", "Graphiques"), index=0)

if view == "Tableau":
	st.subheader("Top 10 — Résumé")
	st.dataframe(filtered_df)

elif view == "Détails":
	st.subheader("Détails")
	for i, row in filtered_df.iterrows():
		st.markdown(f"**{row['Poste']}** — *{row['Entreprise']}*")
		st.write(f"Tâches : {', '.join(row['Liste_taches'])}")
		st.write(f"Complexité : {row['Complexite']} — Salaire estimé : {row['Salaire_annuel_estime']}")
		st.write(f"KPI (Tâches/Salaire) : {row['Ratio_Taches_par_Salaire']}")
		if row['Lien']:
			st.markdown(f"[Voir l'offre]({row['Lien']})")
		st.markdown("---")

else:
	# Graphiques
	st.subheader("Visualisations")

	# Préparer dataframe pour graphiques (appliquer filtre salaire)
	chart_df = filtered_df.copy()
	chart_df['Salaire_annuel_estime'] = pd.to_numeric(chart_df['Salaire_annuel_estime'], errors='coerce')
	chart_df['Ratio_Taches_par_Salaire'] = pd.to_numeric(chart_df['Ratio_Taches_par_Salaire'], errors='coerce')
	chart_df['Complexite'] = pd.to_numeric(chart_df['Complexite'], errors='coerce').fillna(0).astype(int)

	try:
		import altair as alt

		# Bar chart: KPI (Tâches/Salaire) par Poste
		bar = (
			alt.Chart(chart_df)
			.mark_bar()
			.encode(
				x=alt.X('Ratio_Taches_par_Salaire:Q', title='KPI (Tâches/Salaire)'),
				y=alt.Y('Poste:N', sort='-x'),
				color=alt.Color('Complexite:Q', title='Complexité'),
				tooltip=['Poste', 'Entreprise', 'Complexite', 'Salaire_annuel_estime', 'Ratio_Taches_par_Salaire']
			)
			.properties(height=400)
		)

		st.altair_chart(bar, use_container_width=True)

		# Scatter: Complexité vs Salaire
		scatter = (
			alt.Chart(chart_df)
			.mark_circle(size=100)
			.encode(
				x=alt.X('Salaire_annuel_estime:Q', title='Salaire annuel estimé (€)'),
				y=alt.Y('Complexite:Q', title='Complexité'),
				color=alt.Color('Ratio_Taches_par_Salaire:Q', title='KPI'),
				tooltip=['Poste', 'Entreprise', 'Complexite', 'Salaire_annuel_estime', 'Ratio_Taches_par_Salaire']
			)
			.interactive()
			.properties(height=300)
		)

		st.altair_chart(scatter, use_container_width=True)
	except Exception:
		# Fallback simple bar chart avec Streamlit si Altair absent
		st.warning('Altair non disponible — affichage fallback.')
		if chart_df['Ratio_Taches_par_Salaire'].dropna().any():
			st.bar_chart(chart_df.set_index('Poste')['Ratio_Taches_par_Salaire'])