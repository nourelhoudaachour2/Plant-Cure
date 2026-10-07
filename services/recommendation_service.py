import os
import json
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4")


def _fallback_recommendation(plant: str, disease: str, is_healthy: bool):
    if is_healthy:
        return {
            "resume": f"La plante {plant} est saine et ne présente pas de signe pathologique visible.",
            "causes": [],
            "traitement_organique": {
                "nom": "Compost naturel et biostimulant végétal",
                "prix_estime": 14
            },
            "traitement_chimique": {
                "nom": "Aucun traitement chimique nécessaire",
                "prix_estime": 0
            },
            "application": "Appliquer un entretien régulier avec un arrosage modéré, une bonne exposition à la lumière et un enrichissement organique du sol.",
            "duree": "Entretien continu",
            "conseils": [
                "Surveiller les feuilles chaque semaine.",
                "Éviter l’excès d’arrosage.",
                "Favoriser une bonne aération autour de la plante."
            ]
        }

    disease_lower = disease.lower()
    plant_lower = plant.lower()

    if "late_blight" in disease_lower:
        return {
            "resume": f"La plante {plant} présente un mildiou tardif, une maladie agressive favorisée par des conditions fraîches et humides.",
            "causes": [
                "Temps frais et humide prolongé",
                "Propagation rapide des spores par l’eau",
                "Milieu de culture mal ventilé"
            ],
            "traitement_organique": {
                "nom": "Traitement au cuivre autorisé en agriculture organique",
                "prix_estime": 22
            },
            "traitement_chimique": {
                "nom": "Fongicide systémique anti-mildiou",
                "prix_estime": 41
            },
            "application": "Appliquer sur feuillage sec dès l’apparition des premiers symptômes, puis renouveler selon l’évolution de l’infection.",
            "duree": "2 semaines",
            "conseils": [
                "Éviter l’excès d’humidité sur les feuilles.",
                "Retirer les parties très atteintes.",
                "Surveiller quotidiennement la progression."
            ]
        }

    if "early_blight" in disease_lower:
        if "potato" in plant_lower:
            return {
                "resume": "La pomme de terre présente une brûlure précoce, souvent liée à des champignons présents dans le sol ou sur les débris végétaux.",
                "causes": [
                    "Présence de spores fongiques dans le sol",
                    "Feuillage humide pendant une longue durée",
                    "Stress nutritionnel de la plante"
                ],
                "traitement_organique": {
                    "nom": "Pulvérisation à base de bicarbonate et extrait végétal naturel",
                    "prix_estime": 18
                },
                "traitement_chimique": {
                    "nom": "Fongicide protecteur à base de chlorothalonil",
                    "prix_estime": 35
                },
                "application": "Pulvériser sur l’ensemble du feuillage, surtout les parties inférieures, tous les 5 à 7 jours.",
                "duree": "2 à 3 semaines",
                "conseils": [
                    "Éliminer les feuilles fortement touchées.",
                    "Éviter l’arrosage sur le feuillage.",
                    "Améliorer la rotation culturale."
                ]
            }

        return {
            "resume": f"La plante {plant} présente une brûlure précoce, favorisée par l’humidité et la présence d’agents fongiques.",
            "causes": [
                "Humidité prolongée sur les feuilles",
                "Présence de spores fongiques",
                "Faible circulation de l’air"
            ],
            "traitement_organique": {
                "nom": "Pulvérisation de bicarbonate avec savon noir",
                "prix_estime": 16
            },
            "traitement_chimique": {
                "nom": "Fongicide à base de chlorothalonil",
                "prix_estime": 34
            },
            "application": "Pulvériser sur les deux faces des feuilles tous les 5 jours après retrait des parties atteintes.",
            "duree": "2 à 3 semaines",
            "conseils": [
                "Éviter l’arrosage par aspersion.",
                "Supprimer les feuilles les plus atteintes.",
                "Améliorer l’espacement entre les plants."
            ]
        }

    if "bacterial_spot" in disease_lower:
        return {
            "resume": f"La plante {plant} présente une tache bactérienne, une affection qui se propage rapidement en milieu humide.",
            "causes": [
                "Humidité élevée",
                "Contamination bactérienne par éclaboussures",
                "Manipulation de plantes mouillées"
            ],
            "traitement_organique": {
                "nom": "Traitement à base de cuivre homologué en agriculture biologique",
                "prix_estime": 21
            },
            "traitement_chimique": {
                "nom": "Bactéricide spécialisé",
                "prix_estime": 39
            },
            "application": "Pulvériser tôt le matin sur feuillage sec et répéter selon l’intensité des symptômes.",
            "duree": "10 à 15 jours",
            "conseils": [
                "Limiter les éclaboussures d’eau.",
                "Désinfecter les outils de coupe.",
                "Éviter de manipuler les feuilles humides."
            ]
        }

    if "powdery_mildew" in disease_lower:
        return {
            "resume": f"La plante {plant} présente un oïdium, visible sous forme de feutrage blanchâtre sur les feuilles.",
            "causes": [
                "Atmosphère chaude et humide",
                "Faible circulation d’air",
                "Densité excessive de feuillage"
            ],
            "traitement_organique": {
                "nom": "Solution au soufre ou bicarbonate adaptée à l’oïdium",
                "prix_estime": 17
            },
            "traitement_chimique": {
                "nom": "Fongicide anti-oïdium",
                "prix_estime": 31
            },
            "application": "Appliquer sur les zones atteintes tous les 4 à 6 jours jusqu’à amélioration visible.",
            "duree": "1 à 2 semaines",
            "conseils": [
                "Aérer davantage la culture.",
                "Retirer les feuilles très contaminées.",
                "Réduire l’humidité ambiante."
            ]
        }

    return {
        "resume": f"La plante {plant} présente la maladie {disease}.",
        "causes": [
            "Conditions environnementales favorables au pathogène",
            "Stress physiologique de la plante",
            "Présence d’agents infectieux sur le feuillage ou le sol"
        ],
        "traitement_organique": {
            "nom": "Traitement organique ciblé selon le type de maladie",
            "prix_estime": 18
        },
        "traitement_chimique": {
            "nom": "Traitement chimique homologué selon la pathologie",
            "prix_estime": 36
        },
        "application": "Appliquer selon l’état sanitaire observé et répéter suivant la progression des symptômes.",
        "duree": "1 à 3 semaines",
        "conseils": [
            "Réduire l’humidité sur le feuillage.",
            "Retirer les parties très atteintes.",
            "Maintenir une bonne hygiène culturale."
        ]
    }


def generate_recommendation(plant: str, disease: str, is_healthy: bool):
    if not OPENAI_API_KEY:
        return _fallback_recommendation(plant, disease, is_healthy)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        prompt = f"""
Tu es un expert agronome spécialisé dans les maladies des plantes.
Réponds uniquement en JSON valide, sans markdown, sans texte supplémentaire.

Contexte précis:
- plante détectée: {plant}
- maladie détectée: {disease}
- plante saine: {str(is_healthy).lower()}

Consignes:
1. Personnalise totalement la réponse selon la plante et la maladie détectées.
2. Ne donne jamais des causes génériques identiques pour toutes les maladies.
3. Ne donne jamais exactement les mêmes traitements pour toutes les plantes.
4. Le traitement organique doit être réaliste et adapté au cas détecté.
5. Le traitement chimique doit être réaliste et adapté au cas détecté.
6. Les prix doivent être variables selon la solution proposée.
7. Si la plante est saine, ne parle pas de maladie; donne uniquement:
   - un résumé de bon état
   - des conseils de renforcement
   - une solution organique d’entretien
   - un coût estimatif d’entretien
8. Si la plante est malade, donne:
   - un résumé spécifique à cette plante et cette maladie
   - 3 causes probables spécifiques
   - un traitement organique spécifique avec prix estimé en TND
   - un traitement chimique spécifique avec prix estimé en TND
   - une méthode d’application claire
   - une durée estimée
   - 3 conseils utiles adaptés
9. Le contenu doit être professionnel, clair, concis, réaliste, et différent selon chaque diagnostic.

Format JSON exact:
{{
  "resume": "texte",
  "causes": ["c1", "c2", "c3"],
  "traitement_organique": {{
    "nom": "texte",
    "prix_estime": 15
  }},
  "traitement_chimique": {{
    "nom": "texte",
    "prix_estime": 30
  }},
  "application": "texte",
  "duree": "texte",
  "conseils": ["a", "b", "c"]
}}
"""
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt
        )

        text = response.output_text.strip()
        return json.loads(text)

    except Exception:
        return _fallback_recommendation(plant, disease, is_healthy)