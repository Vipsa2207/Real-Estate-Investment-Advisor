# Insight Explorer content: one entry per analysis (chart file, chart type, finding, investor takeaway)

INSIGHTS = {
    "Q1 · Distribution of property prices": dict(
        img="q1_price_distribution.png", chart="Histogram: shows the shape of one numeric column.",
        found="Prices are spread evenly from ₹10 L to ₹500 L (about 5,000 properties in every ₹10 L range). Mean ₹254.6 L ≈ median ₹253.9 L; skewness 0.008.",
        takeaway="Every budget has equal choice. Total price alone does not reveal value, so compare price per sq ft with the city median."),
    "Q2 · Distribution of property sizes": dict(
        img="q2_size_distribution.png", chart="Histogram: comparable with Q1.",
        found="Sizes are spread evenly from 500 to 5,000 sq ft (about 5,500 per 100 sq ft range). Mean 2,750 vs median 2,747 sq ft.",
        takeaway="Small, medium and large homes are equally available. Choose size by your target tenant."),
    "Q3 · Price per sq ft by property type": dict(
        img="q3_ppsf_by_type.png", chart="Box plot: compares median and spread across groups.",
        found="Median ₹/sq ft: Independent House ₹9,305, Apartment ₹9,244, Villa ₹9,190, a gap of only 1.3%.",
        takeaway="Villas cost the same per sq ft as apartments. Choose type by lifestyle, not price."),
    "Q4 · Size vs price relationship": dict(
        img="q4_size_vs_price.png", chart="Scatter plot (5,000-property sample) with trend line on all data.",
        found="No link between size and price (r = −0.003), so bigger homes are cheaper per sq ft (r = −0.615). Good Investment rate: small 8.9%, medium 22.4%, large 40.1%.",
        takeaway="Large homes give the most space per rupee and qualify far more often as Good Investments."),
    "Q5 · Outliers in price per sq ft and size": dict(
        img="q5_outliers.png", chart="Side-by-side box plots: outliers appear as dots beyond 1.5 × IQR.",
        found="19,724 properties (7.9%) are above ₹32,763/sq ft. They are small homes (median 799 sq ft) with high prices (median ₹401 L). Size has no outliers.",
        takeaway="Small homes priced above ₹32,763/sq ft are the most overpriced. Avoid them; the Good Investment rule already excludes them."),
    "Q6 · Average price per sq ft by state": dict(
        img="q6_ppsf_by_state.png", chart="Sorted horizontal bar chart, axis from zero.",
        found="From ₹12,931 (Punjab) to ₹13,252 (Karnataka), a gap of only 2.5%. Delhi and Maharashtra sit low/mid.",
        takeaway="State choice barely changes the price paid. Benchmark against the city median instead."),
    "Q7 · Average property price by city": dict(
        img="q7_price_by_city.png", chart="Sorted horizontal bar chart (42 cities).",
        found="From ₹250.8 L (Cuttack) to ₹258.5 L (Bangalore), a 3.1% gap. Mumbai (₹252.1 L) and New Delhi (₹251.6 L) are among the five cheapest.",
        takeaway="The same budget buys a similar property in any city. This flat pattern confirms the data is synthetic."),
    "Q8 · Median property age by locality": dict(
        img="q8_median_age_by_locality.png", chart="Bar chart of how many localities have each median age.",
        found="99% of the 500 localities have a median age of 17–20 years; 80% sit at exactly 18 or 19. Locality names are codes reused in all 42 cities.",
        takeaway="No locality is genuinely newer. Judge age property by property."),
    "Q9 · BHK distribution across cities": dict(
        img="q9_bhk_by_city.png", chart="Heatmap with diverging colours centred on an equal 20% share.",
        found="Each BHK type is about 20% of every city (all 210 cells between 18.6% and 22.0%). Teal/coral cells are scattered randomly.",
        takeaway="Every BHK type is available in every city. Filter by the BHK your tenants need."),
    "Q10 · Price trends of the top 5 localities": dict(
        img="q10_top5_locality_trend.png", chart="Line chart by 5-year construction period, with the all-property benchmark.",
        found="The top 5 localities average ₹269–275 L, only 6.7% above the market, and swing randomly across build periods (some fall below average). The overall line is flat.",
        takeaway="No locality is consistently premium and newer builds cost no more. There are no sale dates, so this is not market price growth."),
    "Q11 · Correlation between numeric features": dict(
        img="q11_correlation_heatmap.png", chart="Correlation heatmap (lower triangle, full −1 to +1 scale).",
        found="88 of 91 pairs show no link. The 3 links are mechanical: price per sq ft vs size (−0.61) and price (+0.56), and floor vs total floors (+0.50, created by our cleaning swap).",
        takeaway="No feature drives price. Price per sq ft vs the city median is the only reliable value signal."),
    "Q12 · Nearby schools vs price per sq ft": dict(
        img="q12_schools_vs_ppsf.png", chart="Box plot per school count with a median line.",
        found="No effect (r = −0.000). Medians range ₹9,144–9,352 (2.3%); 10 schools (₹9,212) cost no more than 1 school (₹9,261).",
        takeaway="School access comes free, which is a bonus for family-rental investors."),
    "Q13 · Nearby hospitals vs price per sq ft": dict(
        img="q13_hospitals_vs_ppsf.png", chart="Box plot per hospital count with a median line (matches Q12).",
        found="No effect (r = −0.000). Medians range ₹9,128–9,349 (2.4%); 10 hospitals (₹9,196) cost no more than 1 (₹9,256).",
        takeaway="Healthcare access comes free, which suits family and retirement buyers."),
    "Q14 · Price by furnished status": dict(
        img="q14_price_by_furnishing.png", chart="Bar chart of averages (total price has no outliers).",
        found="Unfurnished ₹255.0 L, semi-furnished ₹254.3 L, furnished ₹254.4 L, a 0.3% gap.",
        takeaway="Furnishing comes free. Prefer furnished homes and rent them out immediately."),
    "Q15 · Price per sq ft by facing direction": dict(
        img="q15_ppsf_by_facing.png", chart="Bar chart of medians (₹/sq ft is skewed).",
        found="North ₹9,219, East ₹9,234, South ₹9,225, West ₹9,308, a 1.0% gap. Vastu-preferred North/East are marginally cheapest.",
        takeaway="Buy the most sought-after directions at no premium, which helps resale appeal."),
    "Q16 · Properties per owner type": dict(
        img="q16_owner_type.png", chart="Bar chart with counts and shares (clearer than a pie).",
        found="Broker 83,479, Owner 83,268, Builder 83,253 (~33.3% each). Good Investment rate is 27.0–27.4% for all three.",
        takeaway="Owner listings give the same deal quality without brokerage (often 1–2% of the price)."),
    "Q17 · Properties per availability status": dict(
        img="q17_availability_status.png", chart="Bar chart with counts and shares.",
        found="50/50 split. Prices differ by only 0.3%. Good Investment rate is 38.4% ready vs 16.1% under construction (readiness is one rule criterion).",
        takeaway="There is no under-construction discount, so ready-to-move homes give rental income for the same price."),
    "Q18 · Does parking affect price?": dict(
        img="q18_parking_vs_price.png", chart="Box plot comparing the two groups' full price ranges.",
        found="With parking ₹254.7 L vs without ₹254.4 L (+0.1%). Parking is recorded only as Yes/No.",
        takeaway="Parking comes free, so prefer homes with parking."),
    "Q19 · How amenities affect price per sq ft": dict(
        img="q19_amenities_vs_ppsf.png", chart="Box plot by number of amenities with a median line.",
        found="No effect (r = 0.002). Medians ₹9,207–9,294 (0.9%). Each amenity's premium is between −0.1% and +0.5%.",
        takeaway="Amenity-rich homes (4–5 amenities) cost the same, so they are extra value at no cost."),
    "Q20 · Public transport vs price and investment potential": dict(
        img="q20_transport.png", chart="Two bar panels: median ₹/sq ft and Good Investment rate.",
        found="₹/sq ft is flat (₹9,265 / ₹9,269 / ₹9,205 for Low / Medium / High). Good Investment rate rises 22.7% → 25.4% → 33.6%.",
        takeaway="High-transport homes are the best-value segment: top connectivity at no extra cost."),
    "C1 · What drives a Good Investment?": dict(
        img="p6_1_good_investment_drivers.png", chart="Sorted bar chart of correlations with Good_Investment.",
        found="Below city median is the strongest driver (+0.61), then size (+0.30), security and readiness (+0.25 each), amenities (+0.21). Total price is the strongest negative (−0.40).",
        takeaway="The typical Good Investment is a large, low-priced, ready-to-move home with security and amenities."),
    "C2 · Size vs return, infrastructure vs resale value": dict(
        img="p6_2_size_infra_vs_value.png", chart="Two box-plot panels (the project brief's required pairs).",
        found="Every property earns ~27.6% over 5 years (fixed 5% growth). Size vs gain r = −0.003; infrastructure vs future value r = −0.001.",
        takeaway="Under a fixed growth rate, future value depends only on today's price. Judge quality with the Good Investment rule."),
}

INVESTOR_RECS = [
    ("💰", "Lead with value", "Only buy below the city median price per sq ft.",
     "Strongest driver of a Good Investment (r = +0.61); price per sq ft varies 3.3× within a city."),
    ("📐", "Favour larger homes", "Large homes give the most space per rupee.",
     "Price does not rise with size; 40.1% of large homes qualify vs 8.9% of small."),
    ("🏠", "Choose ready-to-move", "Earn rental income from day one at the same price.",
     "Under-construction homes cost only 0.3% less; 38.4% of ready homes qualify vs 16.1%."),
    ("🚇", "Prioritise high public transport", "Get the best connectivity at no extra cost.",
     "Price per sq ft is flat across transport levels; 33.6% of high-access homes qualify vs 22.7% low."),
    ("🎁", "Collect free quality", "Prefer homes with amenities, schools, hospitals, parking, furnishing and East/North facing.",
     "None of these adds more than 0.5% to price per sq ft."),
    ("⚠️", "Avoid overpriced small homes", "Skip listings above ₹32,763 per sq ft.",
     "19,724 outliers (7.9%): median 799 sq ft at ₹401 lakhs."),
    ("🤝", "Buy direct from owners", "Same deal quality, without brokerage.",
     "Good Investment rate is 27.0–27.4% for all seller types; brokerage is typically 1–2% of the price."),
    ("🗺️", "Don't pay for the city name", "Choose the city for personal or rental reasons, not price.",
     "States differ by 2.5% and cities by 3.1%; Mumbai and Delhi are among the cheapest."),
]

PLATFORM_RECS = [
    ("🏷️", "Show a 'vs city median' badge", "Display each listing's % above or below its city median price per sq ft.",
     "The single clearest value signal found in 250,000 listings."),
    ("⭐", "Rank listings by Deal Score", "Use the 0–5 score to sort listings and flag top picks.",
     "Only 3,006 listings (1.2%) score a perfect 5/5, so a top-pick badge stays exclusive."),
    ("🧾", "Collect richer data", "Add sale dates, RERA status, parking-spot counts and crime data.",
     "Needed for real price trends, location-based growth rates and risk scoring."),
]

REALITY_CHECK = """
- The dataset is **synthetic**: prices, sizes and features are spread evenly, and no feature drives price (88 of 91 feature pairs show no link).
- Location effects are unrealistic (e.g., Mumbai is among the cheapest cities).
- **Good Investment** is a transparent rule (value + at least 2 of 4 quality criteria), not an observed market outcome.
- **Future value** uses one fixed 5% annual growth rate for every property.
- Results demonstrate the method and are **not financial advice**.
"""