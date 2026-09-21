import json
from typing import List, Dict, Any, Optional

class PageSynthesisEngineClient:
    """
    Production-grade dynamic search synthesis and comparison engine.
    Computes mathematical rankings and builds structured Markdown & HTML blocks.
    """
    def __init__(self):
        pass

    def synthesize_page(self, entities: Optional[List[Dict[str, Any]]] = None, ranking_weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        if not entities:
            entities = [
                {
                    "sku": "ROBO-S8", "name": "Roborock S8 MaxV", "price": 1599.0, "rating": 4.8,
                    "specs": {"Suction": "10,000Pa", "Mop": "VibraRise 3.0", "Navigation": "Reactive AI 2.0", "Obstacle": "Vision RGB"},
                    "pros": ["Highest suction", "Robotic corner arm"], "cons": ["High price point"]
                },
                {
                    "sku": "DRM-X40", "name": "Dreame X40 Ultra", "price": 1499.0, "rating": 4.7,
                    "specs": {"Suction": "12,000Pa", "Mop": "MopExtend Dual", "Navigation": "LiDAR 3D", "Obstacle": "Laser Sensor"},
                    "pros": ["Extending side brush", "High water heat"], "cons": ["App connectivity latency"]
                },
                {
                    "sku": "ECO-X2", "name": "Ecovacs Deebot X2", "price": 999.0, "rating": 4.3,
                    "specs": {"Suction": "8,000Pa", "Mop": "OZMO Turbo 2.0", "Navigation": "dToF LiDAR", "Obstacle": "AIVI 3D 2.0"},
                    "pros": ["Square shape fits corners", "Low profile"], "cons": ["Occasional rug snagging"]
                }
            ]

        weights = ranking_weights or {"price_importance": 0.35, "rating_importance": 0.45, "feature_richness": 0.20}
        min_p = min(e["price"] for e in entities) if entities else 1.0

        scored = []
        for e in entities:
            p_score = (min_p / max(1.0, e["price"])) * 10.0
            r_score = (e["rating"] / 5.0) * 10.0
            f_score = min(10.0, len(e.get("specs", {})) * 2.5)
            comp_score = round(
                (p_score * weights.get("price_importance", 0.35) +
                 r_score * weights.get("rating_importance", 0.45) +
                 f_score * weights.get("feature_richness", 0.20)) /
                max(0.1, sum(weights.values())), 2
            )
            scored.append({**e, "composite_score": comp_score})

        scored.sort(key=lambda x: x["composite_score"], reverse=True)
        winner = scored[0]

        all_spec_keys = []
        for e in scored:
            for k in e.get("specs", {}):
                if k not in all_spec_keys: all_spec_keys.append(k)

        # Build Markdown Table
        headers = ["Attribute"] + [e["name"] for e in scored]
        md_lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            "| **Price** | " + " | ".join(f"${e['price']:.2f}" for e in scored) + " |",
            "| **Rating** | " + " | ".join(f"{e['rating']} / 5.0" for e in scored) + " |",
            "| **Overall Score** | " + " | ".join(f"**{e['composite_score']} / 10.0**" for e in scored) + " |"
        ]
        for sk in all_spec_keys:
            md_lines.append(f"| **{sk}** | " + " | ".join(str(e.get("specs", {}).get(sk, "N/A")) for e in scored) + " |")

        # Build HTML summary card
        html_snippet = f"""<div class="p-6 bg-slate-900 border border-slate-700 rounded-xl text-white">
  <div class="flex items-center justify-between mb-4">
    <h3 class="text-xl font-bold">Page Recommendation: {winner['name']}</h3>
    <span class="px-3 py-1 bg-emerald-500 text-white rounded-full text-sm font-semibold">{winner['composite_score']} / 10.0</span>
  </div>
  <p class="text-slate-300 mb-4">Ranked #1 out of {len(scored)} products based on mathematical price-to-performance weighting.</p>
</div>"""

        return {
            "status": "SUCCESS",
            "winner_name": winner["name"],
            "winner_score": winner["composite_score"],
            "ranked_entities": scored,
            "comparison_table_markdown": "\n".join(md_lines),
            "html_embed_snippet": html_snippet,
            "total_evaluated": len(scored)
        }
