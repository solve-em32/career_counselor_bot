import json
import os
import re

# ─── Load all datasets ───────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

with open(os.path.join(DATA_DIR, "careers.json"), "r") as f:
    CAREERS_DB = json.load(f)["careers"]

with open(os.path.join(DATA_DIR, "courses.json"), "r") as f:
    COURSES_DB = json.load(f)["courses"]

with open(os.path.join(DATA_DIR, "aptitude_map.json"), "r") as f:
    APTITUDE_MAP = json.load(f)

# ─── Keyword mapping to career keys ──────────────────────────────────────────
CAREER_KEYWORDS = {
    # ── Original 10 ──
    "pilot": ["commercial pilot", "airline pilot", "cpl", "dgca pilot", "aviation career", "cockpit", "flying school"],
    "software_engineer": ["software engineer", "programmer", "computer science", "cs engineer", "iit cs", "nit cs", "jee tech"],
    "doctor": ["doctor", "mbbs", "medical", "physician", "surgeon", "neet", "hospital", "medicine", "healthcare", "md"],
    "data_scientist": ["data scientist", "machine learning", "ml", "artificial intelligence", "deep learning", "kaggle", "data science"],
    "ias_officer": ["ias", "upsc", "civil service", "collector", "civil servant", "bureaucrat", "ips officer"],
    "ca": ["chartered accountant", "ca exam", "icai exam", "articleship training", "audit career", "taxation career"],
    "lawyer": ["lawyer", "advocate", "legal career", "court practice", "clat exam", "llb degree", "attorney", "barrister"],
    "entrepreneur": ["entrepreneur", "startup founder", "self-employed", "own business", "build startup"],
    "defense_officer": ["indian army", "indian navy", "air force officer", "nda exam", "defense service", "military officer", "cds exam", "armed forces officer", "army officer", "join indian navy"],
    "graphic_designer": ["graphic design", "ui ux", "figma", "photoshop", "illustrator", "nid", "nift", "visual design"],

    # ── Engineering ──
    "aerospace_engineer": ["aerospace engineer", "aeronautical engineer", "hal engineer", "spacecraft engineer", "rocket engineer"],
    "civil_engineer": ["civil engineer", "construction", "bridges", "roads", "infrastructure", "buildings", "structural"],
    "mechanical_engineer": ["mechanical", "automobile", "manufacturing", "tata motors", "maruti", "solidworks", "catia", "machine"],
    "electrical_engineer": ["electrical", "power systems", "electronics", "eee", "circuit", "ntpc", "pgcil", "bhel"],
    "chemical_engineer": ["chemical engineer", "petroleum", "refinery", "iocl", "ongc", "process design", "pharma plant"],
    "marine_engineer": ["marine engineer", "ship engine", "imu", "merchant ship", "offshore", "chief engineer ship"],
    "robotics_engineer": ["robotics", "robot", "ros", "robotic arm", "greyorange", "automation", "mechatronics"],
    "embedded_systems_engineer": ["embedded", "firmware", "microcontroller", "arduino", "rtos", "iot firmware", "arm cortex"],
    "vlsi_engineer": ["vlsi", "chip design", "verilog", "vhdl", "semiconductor", "qualcomm", "intel chip", "eda tools"],

    # ── Technology ──
    "devops_engineer": ["devops engineer", "docker kubernetes", "cicd pipeline", "cloud infrastructure", "jenkins pipeline"],
    "cybersecurity_analyst": ["cybersecurity", "cyber security", "network security", "soc analyst", "vapt", "siem"],
    "ethical_hacker": ["ethical hacker", "penetration testing", "pentest", "bug bounty", "ceh", "oscp", "hackthebox", "kali linux", "ethical hacking", "hacking career"],
    "blockchain_developer": ["blockchain", "solidity", "web3", "defi", "nft", "ethereum", "smart contract", "crypto developer"],
    "game_developer": ["game developer", "unity game dev", "unreal game dev", "game programming", "video game developer"],
    "app_developer": ["app developer", "android", "ios", "flutter", "react native", "mobile app", "kotlin", "swift"],
    "ml_engineer": ["ml engineer", "machine learning engineer", "mlops", "pytorch", "tensorflow", "model deployment"],
    "data_analyst": ["data analyst", "power bi", "tableau", "sql analyst", "excel analytics", "business intelligence"],
    "network_engineer": ["network engineer", "ccna", "ccnp", "routing", "switching", "cisco", "firewall", "lan wan"],
    "cloud_architect": ["cloud architect", "aws", "azure", "gcp", "cloud computing", "solutions architect", "terraform"],
    "iot_engineer": ["iot", "internet of things", "smart devices", "mqtt", "esp32", "raspberry pi", "smart home"],
    "ai_researcher": ["ai researcher", "research scientist", "arxiv", "neurips", "icml", "deepmind", "openai research"],
    "web_developer": ["web developer", "full stack", "react", "nodejs", "html css", "frontend", "backend", "javascript"],
    "technical_writer": ["technical writer", "documentation", "api docs", "user manual", "confluence", "tech writing"],

    # ── Medical ──
    "nurse": ["nurse", "nursing", "gnm", "bsc nursing", "staff nurse", "aiims nursing", "patient care"],
    "pharmacist": ["pharmacist", "pharmacy", "b pharm", "drug", "medicine dispensing", "pharma store"],
    "physiotherapist": ["physiotherapy", "physiotherapist", "bpt", "rehabilitation", "sports physio"],
    "dentist": ["dentist", "dental", "bds", "oral health", "teeth", "orthodontics", "neet dental"],
    "veterinarian": ["vet", "veterinarian", "animal doctor", "bvsc", "pet clinic", "animal treatment"],
    "radiologist": ["radiologist", "radiology", "mri", "ct scan", "xray", "imaging diagnosis"],
    "psychologist": ["clinical psychologist", "counseling psychologist", "mental health therapist", "psychology career", "ma psychology"],
    "social_worker": ["social worker", "msw degree", "bsw degree", "community development", "welfare worker", "tiss social work"],
    "nutritionist": ["nutritionist", "dietitian", "diet plan", "nutrition science", "food and nutrition"],
    "yoga_instructor": ["yoga", "yoga teacher", "ytt", "meditation instructor", "yoga alliance", "pranayama"],
    "fitness_trainer": ["fitness trainer", "personal trainer", "gym trainer", "ace certified", "k11", "issa"],
    "radiographer": ["radiographer", "x ray technician", "bmrit", "radiology technician", "mri technician"],
    "speech_therapist": ["speech therapist", "baslp", "speech language", "stuttering treatment", "aiish"],
    "optometrist": ["optometrist", "b optom", "eye test", "vision correction", "lenskart optometry"],
    "occupational_therapist": ["occupational therapist", "bot degree", "ot therapy", "daily living skills therapy"],
    "lab_technician": ["lab technician", "dmlt", "medical lab", "blood test", "pathology lab", "dr lal labs"],
    "ayurvedic_doctor": ["ayurveda", "bams", "ayurvedic", "herbal medicine", "ayush", "panchkarma"],
    "homeopathic_doctor": ["homeopathy", "bhms", "homeopathic", "homeo doctor", "cch homeopathy"],
    "dentist": ["dentist", "dental", "bds", "teeth", "orthodontics", "oral surgery"],

    # ── Finance & Business ──
    "financial_analyst": ["financial analyst", "cfa", "equity research", "investment analysis", "financial modeling"],
    "investment_banker": ["investment banking", "ib", "mergers acquisitions", "ipo", "goldman sachs", "jp morgan"],
    "actuary": ["actuary", "actuarial", "iai", "risk modeling", "insurance maths", "fellow actuary"],
    "stock_broker": ["stock broker", "equity dealer", "nism", "trading", "dalal street", "demat"],
    "management_consultant": ["management consultant", "mckinsey", "bcg", "bain", "big 4", "deloitte", "ey pwc kpmg"],
    "product_manager": ["product manager", "pm", "apm", "product roadmap", "product strategy", "cpo"],
    "hr_manager": ["hr manager", "human resources", "talent acquisition", "hrm", "hrbp", "chro"],
    "supply_chain_manager": ["supply chain", "logistics manager", "scm", "warehouse", "inventory", "procurement"],
    "operations_research_analyst": ["operations research", "linear programming", "optimization analyst", "industrial engineering"],
    "real_estate_agent": ["real estate", "property agent", "rera agent", "property consultant", "housing sales"],
    "insurance_agent": ["insurance agent", "lic agent", "life insurance", "irdai", "term plan", "health insurance sales"],
    "tax_consultant": ["tax consultant", "gst practitioner", "itr filing", "income tax consultant", "gst filing"],
    "company_secretary": ["company secretary", "cs exam", "icsi", "corporate compliance", "secretarial"],
    "economist": ["economist", "economics", "dse", "igidr", "ies officer", "econometrics", "economic policy"],
    "statistician": ["statistician", "statistics", "isi kolkata", "csir net stats", "css exam", "data statistics"],

    # ── Government & Public Service ──
    "police_officer": ["police", "ips officer", "constable", "si police", "law enforcement", "ssc cpo"],
    "fire_officer": ["fire officer", "firefighter", "fire service", "nebosh", "fire safety", "fire brigade"],
    "customs_officer": ["customs officer", "irs customs", "ssc cgl customs", "import export officer", "smuggling"],
    "income_tax_officer": ["income tax officer", "irs income tax", "it officer", "nadt", "tax raid", "ssc cgl it"],
    "bank_po": ["bank po", "ibps po", "sbi po", "banking officer", "probationary officer", "banking exam"],
    "rbi_officer": ["rbi", "reserve bank", "rbi grade b", "central bank officer", "monetary policy job"],
    "sebi_officer": ["sebi", "securities exchange board", "sebi grade a", "market regulator", "capital market officer"],
    "forest_officer": ["forest officer", "ifs", "indian forest service", "wildlife officer", "forest conservation"],
    "railway_officer": ["railway", "rrb", "irms", "railway engineer", "loco pilot", "railway job"],
    "diplomat": ["diplomat", "ifs foreign service", "ambassador", "embassy", "foreign service", "ifs officer"],

    # ── Creative & Media ──
    "journalist": ["journalist", "reporter", "news anchor", "iimc journalist", "bjmc", "news channel career"],
    "content_writer": ["content writer", "seo writer", "blog writer", "copywriter", "content creation"],
    "digital_marketer": ["digital marketing", "seo", "google ads", "facebook ads", "performance marketing"],
    "social_media_manager": ["social media manager", "instagram manager", "content strategy", "community manager"],
    "pr_professional": ["public relations", "pr agency", "brand communications", "media relations", "crisis comms"],
    "animation_artist": ["vfx artist", "maya animator", "vfx career", "2d animation", "animation studio"],
    "animator_3d": ["3d animator", "character animation", "blender", "maya character", "rigging", "demo reel"],
    "video_editor": ["video editor", "premiere pro", "davinci resolve", "film editing", "youtube editing"],
    "photographer": ["photographer", "photography", "lightroom", "wedding photography", "fashion photography"],
    "art_director": ["art director", "creative director", "ogilvy", "ad agency creative", "visual direction"],
    "actor": ["actor", "acting", "ftii", "nsd", "bollywood", "ott acting", "film career", "theatre"],
    "musician": ["musician", "singer", "music producer", "bollywood music", "composer", "playback singer"],
    "fashion_designer": ["fashion designer", "nift", "clothing design", "fashion house", "garment design"],
    "interior_designer": ["interior designer", "interior design", "3d max", "sketchup", "home decor design"],
    "makeup_artist": ["makeup artist", "bridal makeup", "film makeup", "sfx makeup", "beauty artist"],

    # ── Hospitality & Tourism ──
    "hotel_manager": ["hotel manager", "hospitality", "nchmct", "ihm", "5 star hotel", "general manager hotel"],
    "chef": ["chef", "culinary", "cooking professional", "kitchen", "executive chef", "pastry chef"],
    "event_manager": ["event manager", "event management", "wedding planner", "conference organizer", "wizcraft"],
    "travel_agent": ["travel agent", "tour operator", "iata agent", "travel agency", "tourism business"],
    "cabin_crew": ["cabin crew", "air hostess", "flight attendant", "steward", "airline crew", "frankfinn"],

    # ── Education ──
    "teacher": ["teacher", "school teacher", "b.ed", "ctet", "kvs teacher", "teaching career", "nv teacher"],
    "professor": ["professor", "assistant professor", "ugc net", "college lecturer", "university teacher", "phd teaching"],
    "teacher_educator": ["edtech", "online course creator", "unacademy", "physics wallah", "byju", "online teaching", "udemy creator"],
    "special_educator": ["special educator", "special education", "learning disability", "autism teacher", "rci", "inclusive education"],
    "academic_counselor": ["academic counselor", "study abroad consultant", "overseas education", "college admission counselor", "icef"],
    "librarian": ["librarian", "library science", "mlisс", "blib", "library management", "knowledge manager"],

    # ── Finance Advanced ──
    "venture_capitalist": ["venture capitalist", "venture capital", "vc fund", "startup investor", "seed funding", "series a investor", "fund manager startup", "venture capital career"],
    "private_equity": ["private equity", "pe firm", "lbo", "leveraged buyout", "kkr", "blackstone", "buyout fund"],
    "hedge_fund_manager": ["hedge fund", "quant trader", "quantitative analyst", "prop trading", "algorithmic trading", "quant finance"],
    "credit_analyst": ["credit analyst", "credit risk", "loan assessment", "crisil", "icra", "credit rating", "frm"],
    "wealth_manager": ["wealth manager", "private banking", "hni clients", "cfp", "portfolio management", "wealth advisory"],
    "microfinance_professional": ["microfinance", "mfi", "bandhan bank", "ujjivan", "financial inclusion", "shg lending"],
    "forensic_accountant": ["forensic accountant", "fraud investigator", "cfe", "acfe", "financial fraud", "white collar crime"],
    "compliance_officer": ["compliance officer", "regulatory compliance", "sebi compliance", "rbi guidelines", "ccep certification"],
    "crypto_trader": ["crypto", "cryptocurrency", "bitcoin", "ethereum trading", "defi trading", "coindcx", "wazirx"],
    "personal_finance_advisor": ["personal finance", "ifa", "mutual fund advisor", "amfi", "sip advisor", "investment advisor"],

    # ── Esports & Gaming ──
    "esports_professional": ["esports", "pro gamer", "bgmi pro", "valorant pro", "esports player", "professional gaming", "competitive gaming"],
    "esports_coach": ["esports coach", "gaming coach", "vod review", "team tactics gaming", "pro team coach"],
    "esports_caster": ["esports caster", "gaming commentator", "esports commentary", "nodwin caster", "tournament casting"],
    "gaming_content_creator": ["gaming youtuber", "gaming streamer", "gaming content", "loco streamer", "gaming channel", "mortal scout jonathan"],
    "game_designer": ["game designer", "level designer", "game mechanics", "gdd", "game design document", "mobile game design"],
    "esports_manager": ["esports manager", "team manager gaming", "esports operations", "gaming org management"],

    # ── Graphic Design & Creative ──
    "graphic_novel_artist": ["graphic novel", "comic artist", "manga artist", "webcomic", "sequential art", "comic book"],
    "motion_designer": ["motion designer", "motion graphics", "after effects animation", "cinema 4d", "kinetic typography"],
    "brand_designer": ["brand designer", "logo designer", "visual identity", "brand guidelines", "branding agency"],
    "typeface_designer": ["typeface designer", "font designer", "type design", "glyphs app", "devanagari type", "font foundry"],
    "illustrator": ["illustrator", "digital illustrator", "procreate", "digital art", "editorial illustration"],
    "ux_researcher": ["ux researcher", "user research", "usability testing", "user interviews", "design research"],
    "concept_artist": ["concept artist", "character concept", "environment concept", "entertainment design", "creature design"],
    "product_designer": ["product designer", "industrial designer", "nid product", "physical product design", "consumer product"],
    "textile_designer": ["textile designer", "fabric design", "weave design", "nid textile", "handloom design", "surface design"],

    # ── Research & Science ──
    "science_journalist": ["science journalist", "science writer", "science communicator", "science media", "science content"],
    "clinical_researcher": ["clinical researcher", "clinical trial", "cra", "cro", "clinical research associate", "gcp"],
    "research_scientist": ["research scientist", "csir scientist", "drdo scientist", "government researcher", "scientific officer"],
    "patent_examiner": ["patent examiner", "indian patent office", "cgpdtm", "patent examination", "ip examiner"],
    "space_scientist": ["space scientist", "isro scientist", "icrb", "iist", "satellite scientist", "launch vehicle"],
    "antarctic_researcher": ["antarctic researcher", "polar scientist", "ncpor", "india antarctica expedition", "maitri station"],
    "oceanographer": ["oceanographer", "marine scientist", "nio goa", "ocean research", "marine science"],
    "wildlife_biologist": ["wildlife biologist", "wildlife conservation", "wii dehradun", "tiger reserve", "forest research"],
    "archaeologist": ["archaeologist", "archaeology", "asi archaeologist", "excavation", "deccan college archaeology"],
    "museum_curator": ["museum curator", "art curator", "museum studies", "national museum", "collection management"],

    # ── Social Impact ──
    "ngo_manager": ["ngo manager", "development sector", "ngo professional", "teach for india", "gandhi fellowship", "programme officer"],
    "sustainability_consultant": ["sustainability consultant", "esg analyst", "carbon accounting", "gri reporting", "brsr compliance"],
    "policy_analyst": ["policy analyst", "public policy", "niti aayog", "think tank", "mpp", "policy research"],
    "agrotech_entrepreneur": ["agritech", "agriculture startup", "farm tech", "precision farming", "ninjacart", "dehaat"],

    # ── Sports ──
    "sports_analyst": ["sports analyst", "cricket analytics", "performance analyst", "sports data", "ipl analytics"],
    "sports_psychologist": ["sports psychologist", "athlete mental health", "performance psychology", "sport psychology"],
    "referee_umpire": ["referee", "umpire", "cricket umpire", "football referee", "sports official", "bcci umpire"],
    "talent_scout": ["talent scout", "sports scout", "athlete recruitment", "scouting", "khelo india"],
    "sports_journalist": ["sports journalist", "cricket journalist", "sports reporter", "espncricinfo", "cricbuzz writer"],
    "sports_nutritionist": ["sports nutritionist", "athlete nutrition", "sports dietitian", "cissn", "sports diet"],

    # ── Law ──
    "patent_agent": ["patent agent", "patent filing", "patent drafting", "ip agent", "patent claims"],
    "legal_tech": ["legal tech", "legaltech", "legal software", "contract ai", "legal ai", "legal startup"],
    "mediator": ["mediator", "dispute resolution", "mediation", "iiam", "alternative dispute", "commercial mediation"],
    "arbitrator": ["arbitrator", "commercial arbitration", "diac", "mcia", "international arbitration", "ciarb"],

    # ── Technology Advanced ──
    "data_engineer": ["data engineer", "data pipeline", "apache spark", "kafka", "airflow", "etl pipeline", "big data"],
    "nlp_engineer": ["nlp engineer", "nlp career", "natural language processing engineer", "hugging face developer", "llm engineer"],
    "ar_vr_developer": ["ar vr", "augmented reality", "virtual reality", "xr developer", "meta quest", "vr developer", "arcore arkit"],
    "database_administrator": ["database administrator", "dba", "oracle dba", "sql server", "postgresql admin", "database management"],
    "scrum_master": ["scrum master", "agile coach", "csm", "psm", "agile scrum", "sprint planning"],
    "quality_engineer": ["qa engineer", "quality assurance", "software testing", "selenium", "test automation", "istqb"],
    "site_reliability_engineer": ["site reliability engineer", "site reliability engineer career", "sre engineer", "google sre", "platform reliability"],
    "fintech_developer": ["fintech developer", "payments engineer", "upi developer", "razorpay developer", "banking api"],
    "health_informatics": ["health informatics", "healthcare it", "ehr system", "fhir", "hospital management system", "medical records"],

    # ── Engineering Advanced ──
    "biomedical_engineer": ["biomedical engineer", "medical device", "medical equipment design", "ge healthcare", "philips healthcare"],
    "renewable_energy_engineer": ["renewable energy", "solar engineer", "wind energy", "pvsyst", "adani green", "solar design"],
    "transportation_engineer": ["transportation engineer", "traffic engineer", "highway design", "metro planning", "nhai engineer"],
    "structural_engineer": ["structural engineer", "etabs", "staad pro", "building structure", "bridge design"],
    "geotechnical_engineer": ["geotechnical engineer", "soil mechanics", "foundation design", "plaxis", "tunnel engineering"],
    "mining_engineer": ["mining engineer", "coal india", "nmdc", "mine design", "iit ism dhanbad", "mine safety"],
    "petroleum_engineer": ["petroleum engineer", "oil gas", "ongc engineer", "reservoir engineering", "drilling engineer"],
    "metallurgical_engineer": ["metallurgical engineer", "materials engineer", "steel industry", "sail engineer", "tata steel"],
    "nuclear_engineer": ["nuclear engineer", "barc", "npcil", "nuclear scientist", "oces dgfs", "atomic energy"],
    "nanotechnologist": ["nanotechnology", "nanomaterials", "nanoscience", "nano research", "iit nano"],
    "chartered_engineer": ["chartered engineer", "iei membership", "c.eng", "professional engineer", "licensed engineer"],

    # ── Wellness & Lifestyle ──
    "yoga_therapist": ["yoga therapist", "yoga therapy", "therapeutic yoga", "iayt", "clinical yoga"],
    "meditation_teacher": ["meditation teacher", "mindfulness teacher", "mbsr", "vipassana teacher", "meditation coach"],
    "life_coach": ["life coach", "executive coach", "icf coach", "coaching certification", "career coach"],
    "art_therapist": ["art therapist", "art therapy", "creative therapy", "expressive arts therapy"],

    # ── Architecture & Design ──
    "architect": ["architect", "b arch", "nata", "building design", "spa delhi", "cept", "structural design"],
    "urban_planner": ["urban planner", "city planning", "town planning", "gis planning", "smart city", "b plan"],

    # ── Science & Research ──
    "geologist": ["geologist", "geology", "gsi", "earth science", "rocks minerals", "petroleum geology"],
    "environmental_scientist": ["environmental scientist", "pollution control", "cpcb", "eia", "environmental impact"],
    "astronomer": ["astronomer", "astrophysics", "telescope", "iucaa", "tifr astronomy", "galaxy research"],
    "biologist": ["biologist", "biology research", "molecular biology", "genetics", "ncbs", "life science"],
    "biotechnologist": ["biotechnologist", "biotechnology", "biocon", "serum institute", "crispr", "bioinformatics"],
    "agricultural_scientist": ["agricultural scientist", "icar", "crop science", "agriculture research", "iari"],
    "food_technologist": ["food technologist", "food science", "cftri", "food safety", "fssai", "product development food"],

    # ── Aviation ──
    "pilot_air_traffic_controller": ["air traffic controller", "atc", "aai", "radar control", "aircraft communication"],
    "merchant_navy": ["merchant navy", "nautical science", "deck officer", "ship captain", "master mariner", "merchant ship", "imu cet nautical"],
    "pilot_drone": ["drone pilot", "uav operator", "rpa certificate", "drone services", "agricultural drone", "rpto"],

    # ── Sports & Wellness ──
    "sports_professional": ["professional sportsperson", "cricketer", "football player", "badminton player", "sai sports"],
    "sports_coach": ["sports coach", "cricket coach", "physical education", "pe teacher", "bped", "lnipe"],

    # ── Law & IP ──
    "patent_attorney": ["patent attorney", "ip lawyer", "patent agent", "intellectual property", "patent office"],
    "criminologist": ["criminologist", "forensic science", "gfsu", "crime investigation", "forensic expert", "cbi forensic"],

    # ── Miscellaneous ──
    "psychologist_industrial": ["industrial psychologist", "organizational psychology", "ob psychologist", "talent assessment"],
    "astrologer": ["astrologer", "jyotish", "kundali", "vedic astrology", "horoscope reader"],

    # ── Finance (Advanced) ──
    "venture_capitalist": ["venture capital", "venture capitalist", "vc career", "startup investor", "angel investor", "sequoia"],
    "private_equity": ["private equity", "pe fund", "lbo", "leveraged buyout", "kkr india", "blackstone india"],
    "hedge_fund_manager": ["hedge fund", "quant trader", "quantitative analyst", "prop trading", "optiver", "jane street", "algo trading"],
    "credit_analyst": ["credit analyst", "credit risk", "crisil", "icra", "credit rating", "loan underwriting"],
    "wealth_manager": ["wealth manager", "wealth management", "cfp certified", "private banking", "iifl wealth", "kotak wealth"],
    "microfinance_professional": ["microfinance", "mfi", "bandhan bank", "ujjivan", "self help group", "financial inclusion"],
    "forensic_accountant": ["forensic accountant", "fraud investigation", "cfe certified", "forensic audit", "sfio", "white collar crime"],
    "compliance_officer": ["compliance officer", "compliance career", "regulatory compliance officer", "aml kyc compliance"],
    "crypto_trader": ["crypto trader", "cryptocurrency trading", "bitcoin trading", "defi trading", "coinswitch", "coindcx"],
    "personal_finance_advisor": ["personal finance advisor", "financial planner", "ifa", "mutual fund advisor", "sip advisor", "amfi agent"],

    # ── Esports ──
    "esports_professional": ["esports player", "esports professional", "pro gamer", "bgmi player", "valorant pro", "esports career", "competitive gaming", "esports"],
    "esports_coach": ["esports coach", "esports coaching", "gaming team coach", "valorant coach", "bgmi coach", "pro team coach"],
    "esports_caster": ["esports caster", "gaming commentator", "esports commentary", "caster career"],
    "gaming_content_creator": ["gaming youtuber", "gaming content creator", "game streaming", "gaming creator", "gaming channel"],
    "game_designer": ["game designer", "level designer", "game mechanics design", "gameplay design", "game design document"],
    "esports_manager": ["esports manager", "gaming org manager", "esports operations"],

    # ── Graphic Design (Advanced) ──
    "graphic_novel_artist": ["graphic novel", "comic artist", "manga artist", "webcomic", "sequential art", "comic book"],
    "motion_designer": ["motion designer", "motion graphics", "motion design career", "after effects designer", "cinema 4d"],
    "brand_designer": ["brand designer", "logo designer", "visual identity designer", "brand identity", "brand guidelines"],
    "typeface_designer": ["typeface designer", "font designer", "typography designer", "glyphs app", "type foundry"],
    "illustrator": ["digital illustrator", "procreate artist", "book illustrator", "editorial illustrator", "stock illustrator"],
    "ux_researcher": ["ux researcher", "user researcher", "usability testing", "user interviews", "ux research career"],
    "concept_artist": ["concept artist", "character design artist", "environment concept art", "creature design"],
    "product_designer": ["product designer", "industrial designer", "physical product design", "fusion 360 design"],
    "textile_designer": ["textile designer", "fabric designer", "weave designer", "handloom design", "surface pattern design"],

    # ── Research ──
    "science_journalist": ["science journalist", "science writer", "science communicator", "science reporter"],
    "clinical_researcher": ["clinical researcher", "clinical trial", "clinical research associate", "cra", "cro clinical", "gcp clinical"],
    "research_scientist": ["csir scientist", "drdo scientist", "icar scientist", "government scientist", "scientific officer"],
    "patent_examiner": ["patent examiner", "cgpdtm", "patent office examiner", "patent examination"],
    "space_scientist": ["isro scientist", "icrb exam", "isro engineer", "iist graduate", "chandrayaan scientist"],
    "antarctic_researcher": ["antarctic researcher", "polar scientist", "ncpor", "antarctica expedition", "polar research"],
    "oceanographer": ["oceanographer", "ocean scientist", "nio goa", "marine oceanography", "ocean research"],
    "wildlife_biologist": ["wildlife biologist", "conservation scientist", "wildlife institute", "wii dehradun", "wildlife conservation"],
    "archaeologist": ["archaeologist", "archaeology career", "excavation", "asi archaeologist", "deccan college pune"],
    "museum_curator": ["museum curator", "art curator", "collection curator", "exhibition designer", "national museum career"],
    "nanotechnologist": ["nanotechnology", "nanomaterials scientist", "nano science", "nanomedicine", "cleanroom nano"],

    # ── Social Impact ──
    "ngo_manager": ["ngo", "ngo career", "non profit", "ngo manager", "development sector career"],
    "sustainability_consultant": ["sustainability consultant", "sustainability career", "esg career", "sustainability", "carbon consultant", "green jobs"],
    "policy_analyst": ["policy analyst", "public policy", "think tank", "policy researcher", "niti aayog career"],
    "agrotech_entrepreneur": ["agritech", "agriculture startup", "farm technology", "precision farming", "agri entrepreneur"],

    # ── Sports (Advanced) ──
    "sports_analyst": ["sports analyst", "cricket analyst", "sports data", "ipl data analyst", "performance analyst"],
    "sports_psychologist": ["sports psychologist", "athlete mental coach", "performance psychology", "sports mental health", "ipl team psychologist"],
    "referee_umpire": ["sports referee", "cricket umpire", "football referee", "match official", "sports official"],
    "talent_scout": ["talent scout", "sports talent scout", "player scout", "athlete scouting", "cricket scout"],
    "sports_journalist": ["sports journalist", "cricket journalist", "sports reporter", "espncricinfo", "sports anchor"],
    "sports_nutritionist": ["sports nutritionist", "athlete nutrition", "performance nutrition", "sports dietitian", "cissn certified"],

    # ── Wellness (Advanced) ──
    "yoga_therapist": ["yoga therapist", "therapeutic yoga", "yoga therapy career", "iayt certified", "clinical yoga"],
    "meditation_teacher": ["meditation teacher", "mindfulness teacher", "mbsr teacher", "vipassana teacher", "mindfulness coach"],
    "life_coach": ["life coach", "executive coach", "coaching career", "icf certified coach", "personal development coach"],
    "art_therapist": ["art therapist", "art therapy", "expressive arts therapist", "creative therapy", "art for healing"],

    # ── Law (Advanced) ──
    "patent_agent": ["patent agent", "indian patent agent exam", "patent filing agent", "patent drafting", "ip prosecution"],
    "legal_tech": ["legal tech", "legaltech", "contract automation", "legal software", "legal ai career", "spotdraft"],
    "mediator": ["mediator", "mediation career", "dispute resolution career", "commercial mediator"],
    "arbitrator": ["arbitrator", "commercial arbitrator", "international arbitrator", "diac arbitrator", "ciarb"],

    # ── Technology (Advanced) ──
    "data_engineer": ["data engineer", "data pipeline", "etl engineer", "apache spark", "kafka engineer", "airflow", "bigquery"],
    "nlp_engineer": ["nlp engineer", "natural language processing", "hugging face", "bert gpt engineer", "chatbot engineer"],
    "ar_vr_developer": ["ar vr developer", "augmented reality developer", "virtual reality developer", "xr developer", "meta quest dev"],
    "database_administrator": ["database administrator", "dba", "oracle dba", "postgresql dba", "database management career"],
    "scrum_master": ["scrum master", "agile coach", "csm certification", "agile scrum career", "safe agilist"],
    "quality_engineer": ["qa engineer", "software tester", "quality assurance engineer", "selenium automation", "istqb"],
    "site_reliability_engineer": ["site reliability engineer", "sre engineer", "google sre", "production engineer", "slo sli"],
    "fintech_developer": ["fintech developer", "payments engineer", "upi developer", "payment gateway developer", "fintech career"],
    "health_informatics": ["health informatics", "healthcare it career", "ehr developer", "fhir developer", "abdm career"],

    # ── Education (Advanced) ──
    "teacher_educator": ["edtech career", "online course creator", "udemy instructor", "unacademy educator", "course creator"],
    "special_educator": ["special educator", "special education teacher", "autism educator", "learning disability teacher"],
    "academic_counselor": ["academic counselor", "study abroad consultant", "overseas education consultant", "college counselor"],
    "librarian": ["librarian career", "library science", "mlisc degree", "blib degree", "ugc net library science"],

    # ── Social Sciences ──
    "anthropologist": ["anthropologist", "anthropology career", "ethnography researcher", "anthropological survey india"],
    "geographer": ["geographer", "gis career", "arcgis specialist", "geography career", "remote sensing"],
    "philosopher": ["philosopher", "philosophy", "ai ethics career", "ethics researcher", "logic career"],
    "sociologist": ["sociologist", "sociology career", "social researcher", "market research sociology", "nsso researcher"],
    "political_scientist": ["political scientist", "political science career", "political consultant", "election analyst", "political analyst"],

    # ── Engineering (Advanced) ──
    "biomedical_engineer": ["biomedical engineer", "medical device engineer", "ge healthcare career", "biomed engineer"],
    "renewable_energy_engineer": ["renewable energy", "solar energy career", "wind energy career", "clean energy engineer", "solar engineer"],
    "transportation_engineer": ["transportation engineer", "traffic engineer", "highway engineer", "metro design engineer", "nhai career"],
    "structural_engineer": ["structural engineer", "etabs engineer", "staad pro engineer", "building structure engineer"],
    "geotechnical_engineer": ["geotechnical engineer", "soil engineer", "foundation engineer", "tunnel geotechnics"],
    "mining_engineer": ["mining engineer", "coal india engineer", "mine design engineer", "underground mine engineer"],
    "petroleum_engineer": ["petroleum engineer", "oil gas engineer", "ongc petroleum", "reservoir engineer", "drilling engineer"],
    "metallurgical_engineer": ["metallurgical engineer", "materials engineer", "steel plant engineer", "alloy designer"],
    "nuclear_engineer": ["nuclear engineer", "barc career", "npcil career", "nuclear science career", "oces dgfs exam"],
    "chartered_engineer": ["chartered engineer", "iei membership", "ceng designation", "institution of engineers"],

    # ── Creative (Advanced) ──
    "fashion_stylist": ["fashion stylist", "celebrity stylist", "editorial stylist", "personal stylist career"],
    "voice_actor": ["voice actor", "dubbing artist", "voice over artist", "audiobook narrator", "animated voice"],
    "radio_jockey": ["radio jockey", "rj career", "fm radio career", "podcast host career", "radio mirchi career"],
    "stand_up_comedian": ["stand up comedian", "stand up comedy", "comedian", "comedy career", "open mic performer"],
    "food_blogger": ["food blogger", "food youtuber", "food content creator", "restaurant reviewer career"],
    "travel_blogger": ["travel blogger", "travel youtuber", "travel influencer career", "travel vlogger"],
    "indie_filmmaker": ["indie filmmaker", "independent filmmaker", "film director", "indie film", "nfdc filmmaker"],
    "screenwriter": ["screenwriter", "script writer", "screenplay", "ott script writer", "bollywood writer"],

    # ── Specialised ──
    "gemologist": ["gemologist", "gemstone career", "diamond grading", "gia certification career", "jewellery design"],
    "ethical_fashion": ["ethical fashion designer", "sustainable fashion career", "slow fashion", "fair trade fashion designer"],
}

# ─── Intent keywords ─────────────────────────────────────────────────────────
INTENT_KEYWORDS = {
    "career_info":      ["want to be", "want to become", "interested in", "career in",
                         "how to become", "what is", "tell me about", "i want"],
    "roadmap":          ["roadmap", "path", "steps", "how do i", "how to start",
                         "guide me", "what should i do"],
    "salary":           ["salary", "pay", "income", "earn", "money", "package", "lpa"],
    "colleges":         ["college", "university", "institute", "admission", "best college",
                         "where to study", "top institute"],
    "dont_know":        ["don't know", "confused", "no idea", "not sure", "help me decide",
                         "suggest", "what should i", "which career", "clueless"],
    "alternatives":     ["alternative", "backup", "other option", "if i fail", "plan b"],
    "courses":          ["course", "learn", "online", "youtube", "coursera", "udemy",
                         "resource", "where to learn"],
    "greeting":         ["hello", "hi", "hey", "good morning", "good evening", "namaste",
                         "hii", "helo"],
    "thanks":           ["thank", "thanks", "helpful", "awesome", "great", "perfect"],
    "exit":             ["bye", "exit", "quit", "goodbye", "close", "stop"]
}

# ─── Detect which career is being mentioned ──────────────────────────────────
def detect_career(user_input: str) -> str | None:
    text = user_input.lower()

    # Step 1: keyword-based scoring with tiebreaker (longest keyword match wins)
    scores = {}
    longest_match = {}
    for career_key, keywords in CAREER_KEYWORDS.items():
        matched = [kw for kw in keywords if kw in text]
        if matched:
            scores[career_key] = len(matched)
            longest_match[career_key] = max(len(kw) for kw in matched)
    if scores:
        max_score = max(scores.values())
        top = {k: v for k, v in scores.items() if v == max_score}
        # Tiebreak: career whose longest matched keyword is longest wins
        return max(top, key=lambda k: longest_match[k])

    # Step 2: match career_key directly e.g. "venture capitalist" → venture_capitalist
    for career_key in CAREERS_DB:
        readable = career_key.replace("_", " ")
        if readable in text:
            return career_key

    # Step 3: match career title from JSON e.g. "Venture Capitalist (VC)"
    for career_key, career_data in CAREERS_DB.items():
        core_title = career_data["title"].lower().split("(")[0].strip()
        if len(core_title) > 4 and core_title in text:
            return career_key

    # Step 4: all main words of career key found in text
    for career_key in CAREERS_DB:
        parts = [p for p in career_key.replace("_", " ").split() if len(p) > 3]
        if len(parts) >= 2 and all(p in text for p in parts):
            return career_key

    return None

# ─── Detect intent ────────────────────────────────────────────────────────────
def detect_intent(user_input: str) -> str:
    text = user_input.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return intent
    return "general"

# ─── Format career full info ─────────────────────────────────────────────────
def format_career_overview(career_key: str) -> str:
    c = CAREERS_DB[career_key]
    lines = []
    lines.append(f"\n{'='*55}")
    lines.append(f"  🎯  {c['title'].upper()}")
    lines.append(f"{'='*55}")
    lines.append(f"\n📌 What is it?\n   {c['description']}")

    # Requirements
    req = c["requirements"]
    lines.append(f"\n📋 Basic Requirements:")
    lines.append(f"   • Minimum Education : {req['min_education']}")
    if req["mandatory_subjects"]:
        lines.append(f"   • Mandatory Subjects: {', '.join(req['mandatory_subjects'])}")
    if req["min_percentage"]:
        lines.append(f"   • Minimum Marks    : {req['min_percentage']}%")
    lines.append(f"   • Age Range        : {req['age_range']}")
    if req.get("medical") and req["medical"] != "None":
        lines.append(f"   • Medical          : {req['medical']}")

    # Roadmap
    lines.append(f"\n🗺️  Step-by-Step Roadmap:")
    for i, step in enumerate(c["roadmap"], 1):
        lines.append(f"   {i}. {step}")

    # Entrance exams
    if c.get("entrance_exams"):
        lines.append(f"\n📝 Key Exams to Clear:")
        for exam in c["entrance_exams"]:
            lines.append(f"   • {exam}")

    # Salary
    sal = c["salary"]
    lines.append(f"\n💰 Salary in India:")
    lines.append(f"   • Fresher  : {sal['fresher']}")
    lines.append(f"   • Mid-level: {sal['mid_level']}")
    lines.append(f"   • Senior   : {sal['senior']}")

    # Cost & duration
    lines.append(f"\n⏱️  Duration : {c['duration']}")
    lines.append(f"💸 Cost Est : {c['cost_estimate']}")

    # Top institutes
    lines.append(f"\n🏛️  Top Institutes:")
    for inst in c["top_institutes"][:4]:
        lines.append(f"   • {inst}")

    # Pros & Cons
    lines.append(f"\n✅ Pros:")
    for p in c["pros"]:
        lines.append(f"   + {p}")
    lines.append(f"\n❌ Cons:")
    for con in c["cons"]:
        lines.append(f"   - {con}")

    # Skills
    lines.append(f"\n🧠 Skills You Need:")
    lines.append(f"   {' | '.join(c['skills_needed'])}")

    lines.append(f"\n{'='*55}")
    lines.append("💡 Type 'alternatives' to see backup options")
    lines.append("💡 Type 'courses' to see what you can start learning today")
    lines.append(f"{'='*55}\n")

    return "\n".join(lines)

# ─── Format alternatives ──────────────────────────────────────────────────────
def format_alternatives(career_key: str) -> str:
    c = CAREERS_DB[career_key]
    lines = [f"\n🔄 Backup Options if {c['title']} doesn't work out:\n"]
    for alt in c["alternatives_if_fail"]:
        lines.append(f"   → {alt}")
    lines.append("\nRemember: Every backup option is a career in itself, not a failure! 💪\n")
    return "\n".join(lines)

# ─── Format courses ────────────────────────────────────────────────────────────
def format_courses(career_key: str) -> str:
    career_info = CAREERS_DB[career_key]
    category = career_info["category"]

    lines = [f"\n📚 Courses to start your journey as a {career_info['title']}:\n"]
    found = False

    for cat, course_list in COURSES_DB.items():
        for course in course_list:
            if career_key in course.get("good_for", []) or cat == category:
                lines.append(f"   📖 {course['name']}")
                lines.append(f"      Platform  : {course['platform']} ({course['provider']})")
                lines.append(f"      Level     : {course['level']}")
                lines.append(f"      Duration  : {course['duration']}")
                lines.append(f"      Cost      : {course['cost']}")
                lines.append(f"      Link      : {course['link']}\n")
                found = True

    if not found:
        lines.append("   Start with YouTube searches and free resources for now.")
        lines.append("   Search: '{} tutorial for beginners India'".format(career_info["title"]))

    return "\n".join(lines)

# ─── Interest-based assessment ────────────────────────────────────────────────
def run_interest_assessment() -> str:
    print("\n" + "="*55)
    print("  🧩  CAREER INTEREST ASSESSMENT")
    print("="*55)
    print("\nI'll ask you 3 quick questions to suggest the best careers for you.\n")

    # Q1 - Stream
    print("Q1. What is your current education level / stream?")
    print("   1. 12th - PCM (Physics, Chemistry, Maths)")
    print("   2. 12th - PCB (Physics, Chemistry, Biology)")
    print("   3. 12th - Commerce")
    print("   4. 12th - Arts / Humanities")
    print("   5. Graduate / College student")

    stream_choice = input("\n   Your choice (1-5): ").strip()
    stream_map = {
        "1": "PCM", "2": "PCB", "3": "Commerce",
        "4": "Arts", "5": "Graduation"
    }
    stream = stream_map.get(stream_choice, "Graduation")

    # Q2 - Interest area
    print("\nQ2. What kind of work excites you most?")
    print("   1. Maths, science, solving logical problems")
    print("   2. Art, design, music, creative work")
    print("   3. Talking to people, leading, public speaking")
    print("   4. Business, money, markets, trading")
    print("   5. Helping sick people, serving society")
    print("   6. Computers, gadgets, coding, tech")

    interest_choice = input("\n   Your choice (1-6): ").strip()
    interest_map = {
        "1": "maths_science", "2": "arts_creativity",
        "3": "people_communication", "4": "business_money",
        "5": "helping_others", "6": "technology_gadgets"
    }
    interest_key = interest_map.get(interest_choice, "maths_science")

    # Q3 - Income preference
    print("\nQ3. What matters most to you in a career?")
    print("   1. Very high salary (money first)")
    print("   2. Stability and government job")
    print("   3. Creative freedom and independence")
    print("   4. Making an impact on society")

    priority = input("\n   Your choice (1-4): ").strip()

    # ─── Generate result ───
    interest_data = APTITUDE_MAP["interest_to_career_map"].get(interest_key, {})
    stream_data = APTITUDE_MAP["stream_to_career_map"].get(stream, {})

    # Find common careers between interest and stream
    interest_careers = set(interest_data.get("careers", []))
    stream_careers = set(stream_data.get("best_careers", []))
    common = list(interest_careers & stream_careers)

    if not common:
        common = list(interest_careers)[:3]

    lines = ["\n" + "="*55]
    lines.append("  🎉  YOUR PERSONALIZED CAREER RECOMMENDATIONS")
    lines.append("="*55)
    lines.append(f"\n{interest_data.get('message', 'Great choices!')}")
    lines.append(f"\nBased on your stream ({stream}) and interests, here are your top careers:\n")

    for i, career_key in enumerate(common[:3], 1):
        if career_key in CAREERS_DB:
            c = CAREERS_DB[career_key]
            sal = c["salary"]
            lines.append(f"   {i}. {c['title']}")
            lines.append(f"      📈 Starting Salary: {sal['fresher']}")
            lines.append(f"      🎯 Senior Salary  : {sal['senior']}")
            lines.append(f"      ⏱️  Time to Job    : {c['duration']}\n")

    if stream_data.get("entrance_exams"):
        lines.append(f"📝 Key exams for your stream ({stream}):")
        for exam in stream_data["entrance_exams"]:
            lines.append(f"   • {exam}")

    lines.append("\n💡 Type any career name above for full details and roadmap!")
    lines.append("="*55 + "\n")

    return "\n".join(lines)

# ─── Greeting ────────────────────────────────────────────────────────────────
def get_greeting() -> str:
    return """
╔══════════════════════════════════════════════════════╗
║         🎓  CAREER COUNSELOR BOT  🎓                ║
║         Your Personal Career Guide                  ║
╚══════════════════════════════════════════════════════╝

Hey there! I'm your AI Career Counselor. 👋
I can help you with:

  🎯  Career exploration  → "I want to become a pilot"
  🗺️  Roadmaps           → "How do I become a software engineer?"
  💰  Salary info        → "What is the salary of a doctor?"
  🏛️  College guidance   → "Best colleges for CA in India?"
  🔄  Backup options     → "Alternatives to IAS if I fail"
  📚  Course recs        → "Courses to become a data scientist"
  🧩  Not sure?          → Type "suggest" or "I don't know"

Just type naturally — I understand you!

Type 'exit' or 'quit' to leave.
──────────────────────────────────────────────────────
"""
