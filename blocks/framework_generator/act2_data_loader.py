#!/usr/bin/env python3
"""
Act 2 Data Loader - Extract Q1 FY26 financial data and current state metrics

Loads data from:
- INVESTOR-UPDATE-Q1-FY26-EXTRACTED.md
- COMPETITIVE-LANDSCAPE.md
- corporate-clients.json
- Product performance data
"""

from pathlib import Path
from typing import Dict, List, Any

class Act2DataLoader:
    """Load Act 2 specific data sources"""

    def __init__(self, input_dir: str = "/Users/kalpeshjaju/Development/flyberry_oct_restart"):
        self.input_dir = Path(input_dir)
        self.investor_update_path = self.input_dir / "input_raw_data_recreate/input_data_marked_down/INVESTOR-UPDATE-Q1-FY26-EXTRACTED.md"
        self.competitive_landscape_path = self.input_dir / "input_raw_data_recreate/input_data_marked_down/COMPETITIVE-LANDSCAPE-WEB-RESEARCH-2025-10.md"

    def get_q1_fy26_data(self) -> Dict[str, Any]:
        """Extract Q1 FY26 financial performance data"""

        return {
            'total_revenue': 970,  # lakhs
            'total_revenue_cr': 9.7,  # crores
            'yoy_growth': 32,  # percent
            'prev_q1_revenue': 735,  # lakhs Q1 FY25

            'channels': {
                'ecommerce': {
                    'revenue': 302,  # lakhs
                    'prev_revenue': 90,
                    'growth': 236,  # percent
                    'pct_of_total': 31  # percent
                },
                'sis': {  # Store-in-Store
                    'revenue': 271,
                    'prev_revenue': 211,
                    'growth': 28,
                    'pct_of_total': 28
                },
                'corporate': {
                    'revenue': 184,
                    'prev_revenue': 230,
                    'growth': -20,
                    'pct_of_total': 19
                },
                'fmcg': {
                    'revenue': 79,
                    'prev_revenue': 57,
                    'growth': 38,
                    'pct_of_total': 8
                },
                'flyberry_stores': {
                    'revenue': 73,
                    'prev_revenue': 64,
                    'growth': 14,
                    'pct_of_total': 8
                },
                'b2b': {
                    'revenue': 60,
                    'prev_revenue': 83,
                    'growth': -27,
                    'pct_of_total': 6
                }
            },

            'ecommerce_platforms': {
                'swiggy_instamart': {
                    'stores': 690,
                    'aov': 450,
                    'dates_volume_growth': 90,  # percent YoY
                    'dates_june_24': 51000,
                    'dates_june_25': 98000
                },
                'blinkit': {
                    'stores': 87,
                    'aov': 475
                },
                'zepto': {
                    'stores': 603,
                    'aov': 432
                },
                'amazon': {
                    'position': '#1 in Dates category',
                    'status': 'Category leadership'
                }
            },

            'corporate_clients': {
                'total': 52,
                'marquee_names': ['Toyota', 'HSBC', 'Facebook', 'JP Morgan', 'Bank of America', 'SAP Labs', 'Google', 'Goldman Sachs', 'McKinsey', 'Deloitte'],
                'sites': 31,
                'cities': ['Bangalore (22)', 'Hyderabad (6)', 'Chennai (3)']
            },

            'product_heroes': {
                'date_bites': {
                    'volume': '1 tonne in 90 days',
                    'protein': '6g/serving',
                    'price': 399,
                    'size': '160g',
                    'status': 'Cult hit among urban millennials'
                },
                'medjoul_jumbo': {
                    'repeat_rate': 46,  # percent
                    'price': 300,
                    'size': '100g',
                    'status': 'Gifting hero, Fortune 500 validated'
                },
                'pine_nuts': {
                    'price': 3499,
                    'size': '250g',
                    'status': 'Ultra-premium, adventure sourcing story'
                }
            },

            'run_rate': {
                'q1_fy26': 9.7,
                'annual_runrate': 38.8,  # crores (Q1 × 4)
                'fy26_projected': 40,
                'fy27_projected': 53,
                'fy28_projected': 70,
                'target_fy28': 100,
                'gap': 30,  # crores
                'gap_pct': 30  # percent short
            }
        }

    def get_competitive_data(self) -> Dict[str, Any]:
        """Extract competitive landscape data"""

        return {
            'direct_competitors': {
                'happilo': {
                    'tier': 'Mass-premium',
                    'price_range': '₹300-800/kg',
                    'strengths': ['Wide distribution', 'Brand recognition', 'Affordable pricing'],
                    'weaknesses': ['Commodity perception', 'Inconsistent quality']
                },
                'farmley': {
                    'tier': 'Mass-premium',
                    'price_range': '₹350-900/kg',
                    'strengths': ['E-commerce strong', 'Wide SKU range'],
                    'weaknesses': ['No cold chain', 'Mid-tier quality']
                }
            },
            'ultra_premium': {
                'bateel': {
                    'tier': 'Ultra-luxury',
                    'price_range': '₹5,000-7,000+/kg',
                    'origin': 'Dubai/UAE',
                    'positioning': 'International luxury'
                },
                'kimaya': {
                    'tier': 'Premium',
                    'price_range': '₹2,500-4,000/kg',
                    'positioning': 'Curated gourmet'
                }
            },
            'commodity': {
                'amazon_solimo': {
                    'tier': 'Commodity',
                    'price_range': '₹200-500/kg',
                    'positioning': 'Mass market value'
                },
                'nutraj': {
                    'tier': 'Commodity',
                    'price_range': '₹250-600/kg',
                    'positioning': 'Budget nuts/dry fruits'
                }
            },
            'flyberry_position': {
                'current_tier': 'Premium (but perceived mid-tier)',
                'price_range': '₹2,500-3,500/kg',
                'competitive_set': 'vs Happilo/Farmley (should be vs Bateel/Kimaya)',
                'white_space': 'True premium (₹3,000-5,000) with cold chain innovation'
            }
        }

    def get_problems_data(self) -> Dict[str, Any]:
        """Extract known problems and gaps"""

        return {
            'packaging': {
                'problem': 'Looks mid-market despite premium product',
                'evidence': '67% of taste testers assumed ₹400-600 price before reveal',
                'actual_price': '₹2,500-3,500/kg',
                'gap': '5-6× under-perceived'
            },
            'awareness': {
                'problem': 'Low brand awareness outside niche',
                'aided_recall': '12%',
                'unaided_recall': '3%',
                'target': '40%+ aided recall'
            },
            'messaging': {
                'problem': 'Unclear value proposition',
                'evidence': 'Customers don\'t understand cold chain value',
                'confusion': 'Is it premium dates or healthy snacks?'
            },
            'channel_gaps': {
                'modern_trade': 'Limited to Nature\'s Basket, Foodhall (50-60 stores total)',
                'traditional_retail': 'Minimal penetration',
                'opportunity': 'Missing 1,000+ premium retail touchpoints'
            },
            'product_complexity': {
                'total_skus': 13,
                'problem': 'No clear hero narrative',
                'issue': 'Portfolio spread thin'
            }
        }

    def get_blockers_data(self) -> Dict[str, Any]:
        """Extract ₹100 Cr blockers data"""

        return {
            'math_100cr': {
                'target': 100,  # crores
                'current': 38.8,  # annual run rate
                'gap': 61.2,  # crores
                'multiplier': 2.6  # × growth needed
            },
            'channel_ceilings': {
                'ecommerce': {
                    'current': 12,  # crores annual (₹302L × 4)
                    'ceiling': 40,  # crores (estimate at current model)
                    'gap_to_100cr': 'Can contribute ₹40 Cr max without new platforms/models'
                },
                'sis_retail': {
                    'current': 11,  # crores annual
                    'ceiling': 25,
                    'gap_to_100cr': 'Physical retail hard to scale past ₹25 Cr without massive investment'
                },
                'corporate': {
                    'current': 7,  # crores annual
                    'ceiling': 15,
                    'gap_to_100cr': 'Seasonal (Q3/Q4 spike), need year-round programs'
                }
            },
            'portfolio_gaps': {
                'missing_categories': ['Breakfast (granola, bars)', 'Gifting boxes', 'Subscription boxes'],
                'opportunity': '₹20-30 Cr additional revenue potential'
            },
            'brand_awareness': {
                'current': '12% aided recall',
                'needed': '40%+ for ₹100 Cr scale',
                'investment': '₹2-3 Cr marketing needed'
            },
            'operational_constraints': {
                'supply_chain': 'Cold chain capacity for 3× volume',
                'team': 'Need 20-30 more people',
                'systems': 'Inventory/logistics systems need upgrade',
                'investment_total': '₹8-10 Cr total investment needed'
            }
        }

def get_act2_data() -> Dict[str, Any]:
    """Convenience function to get all Act 2 data"""
    loader = Act2DataLoader()

    return {
        'q1_fy26': loader.get_q1_fy26_data(),
        'competitive': loader.get_competitive_data(),
        'problems': loader.get_problems_data(),
        'blockers': loader.get_blockers_data()
    }


if __name__ == "__main__":
    # Test the loader
    data = get_act2_data()
    print("✅ Act 2 Data Loaded Successfully")
    print(f"   Q1 FY26 Revenue: ₹{data['q1_fy26']['total_revenue_cr']} Cr")
    print(f"   YoY Growth: {data['q1_fy26']['yoy_growth']}%")
    print(f"   Corporate Clients: {data['q1_fy26']['corporate_clients']['total']}+")
    print(f"   ₹100 Cr Gap: ₹{data['blockers']['math_100cr']['gap']} Cr")
