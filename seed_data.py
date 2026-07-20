import os
import sys
import shutil
import django

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import User
from portfolio.models import PersonalInfo, Skill, Project

def seed():
    print("Seeding database...")
    
    # 1. Create/Update Superuser only if ADMIN_PASSWORD environment variable is defined
    admin_user = os.environ.get("ADMIN_USERNAME", "admin")
    admin_email = os.environ.get("ADMIN_EMAIL", "issah.boresa.stu@uenr.edu.gh")
    admin_pass = os.environ.get("ADMIN_PASSWORD")

    if admin_pass:
        user, created = User.objects.get_or_create(username=admin_user)
        user.set_password(admin_pass)
        user.email = admin_email
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"Superuser '{admin_user}' updated safely from environment variables.")

    # Setup Media Files
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(base_dir)
    media_dir = os.path.join(base_dir, "media")
    profile_dir = os.path.join(media_dir, "profile")
    resumes_dir = os.path.join(media_dir, "resumes")
    
    os.makedirs(profile_dir, exist_ok=True)
    os.makedirs(resumes_dir, exist_ok=True)

    # Copy photo & CV if available
    src_photo = os.path.join(root_dir, "boresa.jpeg")
    src_cv = os.path.join(root_dir, "IssahSalim_CV.pdf")
    
    dst_photo_rel = ""
    if os.path.exists(src_photo):
        dst_photo = os.path.join(profile_dir, "boresa.jpeg")
        shutil.copy(src_photo, dst_photo)
        dst_photo_rel = "profile/boresa.jpeg"
    elif os.path.exists(os.path.join(profile_dir, "boresa.jpeg")):
        dst_photo_rel = "profile/boresa.jpeg"

    dst_cv_rel = ""
    if os.path.exists(src_cv):
        dst_cv = os.path.join(resumes_dir, "IssahSalim_CV.pdf")
        shutil.copy(src_cv, dst_cv)
        dst_cv_rel = "resumes/IssahSalim_CV.pdf"
    elif os.path.exists(os.path.join(resumes_dir, "IssahSalim_CV.pdf")):
        dst_cv_rel = "resumes/IssahSalim_CV.pdf"

    # 2. Seed Personal Info
    PersonalInfo.objects.all().delete()
    info = PersonalInfo.objects.create(
        name="Issah Abdulsalim Boresa",
        role="Full-Stack & AI/ML Developer",
        email="issah.boresa.stu@uenr.edu.gh",
        phone="(059) 6878044",
        location="Bono-East, Yeji, Ghana",
        linkedin="https://linkedin.com/in/issahsalim",
        github="https://github.com/issahsalim",
        youtube="https://youtube.com/@issahsalim",
        bio="Full Stack Developer with over 5 years of experience building scalable web and mobile applications. Strategically integrates AI-assisted development tools (e.g., Copilot, CLI assistants) and machine learning models (ViT, ResNet50, Random Forest) to boost productivity, improve code efficiency, and streamline end-to-end workflows.",
        profile_image=dst_photo_rel,
        resume=dst_cv_rel
    )
    print(f"Created Personal Info for {info.name}")

    # 3. Seed Skills
    Skill.objects.all().delete()
    skills_data = [
        # Frontend
        ("React JS", "Frontend", 95, 1),
        ("Next JS", "Frontend", 92, 2),
        ("Expo React Native", "Frontend", 88, 3),
        ("HTML5 / CSS3 / JavaScript", "Frontend", 98, 4),
        ("Tailwind CSS / Bootstrap", "Frontend", 94, 5),
        ("Responsive Web Design & SEO", "Frontend", 90, 6),
        # Backend
        ("Django & Django REST Framework", "Backend", 95, 1),
        ("RESTful APIs & JWT Auth", "Backend", 95, 2),
        ("PostgreSQL & MySQL", "Backend", 90, 3),
        ("Python", "Backend", 96, 4),
        # AI / ML
        ("Vision Transformer (ViT-B/16) & ResNet50", "AI_ML", 85, 1),
        ("Random Forest & Decision Trees", "AI_ML", 88, 2),
        ("Gemini Generative AI Integration", "AI_ML", 90, 3),
        ("Scikit-Learn, Pandas & NumPy", "AI_ML", 88, 4),
        # Tools & Other
        ("Git & GitHub", "Tools_Other", 95, 1),
        ("Docker Containerization", "Tools_Other", 85, 2),
        ("AI-Assisted Development (Copilot, CLI)", "Tools_Other", 98, 3),
        ("Video Editing", "Tools_Other", 80, 4),
    ]

    for name, cat, level, order in skills_data:
        Skill.objects.create(name=name, category=cat, level=level, order=order)
    print(f"Seeded {len(skills_data)} skills.")

    # 4. Seed Projects
    Project.objects.all().delete()
    projects_data = [
        {
            "title": "ProjectFreeStress",
            "subtitle": "Academic Marketplace Platform",
            "description": "A web-based marketplace platform where students can buy, sell, and request academic project work. The platform connects students needing project assistance with those offering completed work, featuring clean responsive UI and secure transaction flows.",
            "tech_stack": "Django, Django REST Framework, React JS, PostgreSQL, Bootstrap, HTML, CSS, JavaScript",
            "live_url": "https://projectfreestress.com",
            "github_url": "https://github.com/issahsalim/projectfreestress",
            "order": 1
        },
        {
            "title": "Study Planner",
            "subtitle": "Student Productivity Tool",
            "description": "A web application helping students manage study schedules, join collaborative study groups, and track tasks efficiently. Includes schedule management, group collaboration tools, and task tracking with visual progress indicators.",
            "tech_stack": "Django, React JS, PostgreSQL, Bootstrap, HTML, CSS, JavaScript",
            "live_url": "https://studyplanner.app",
            "github_url": "https://github.com/issahsalim/study-planner",
            "order": 2
        },
        {
            "title": "MCH Yeji — Hospital Website",
            "subtitle": "Institutional & Healthcare Platform",
            "description": "Designed and developed a fully responsive website for Mathias Catholic Hospital, Yeji. Features online appointment booking, job application portal, and dedicated dashboards for HR staff and Doctors to manage workflows efficiently.",
            "tech_stack": "Django, Django REST Framework, React JS, MySQL, Bootstrap, HTML, CSS, JavaScript",
            "live_url": "https://mchyeji.org",
            "github_url": "https://github.com/issahsalim/mch-yeji",
            "order": 3
        },
        {
            "title": "AI-Powered Glaucoma Detection System",
            "subtitle": "Clinical-Grade Medical Diagnosis Tool",
            "description": "A clinical-grade dual-engine AI platform for automatic glaucoma detection from retinal fundus images. Integrates Vision Transformer (ViT-B/16) (81% validation accuracy) and fine-tuned ResNet50 CNN (79% accuracy), trained on over 17,000 fundus images. Includes Python/Django API backend and Expo React Native mobile app.",
            "tech_stack": "Python, Django REST Framework, Vision Transformer (ViT-B/16), ResNet50 CNN, Expo React Native, Docker, JWT Authentication",
            "live_url": "",
            "github_url": "https://github.com/issahsalim/glaucoma-detection",
            "order": 4
        },
        {
            "title": "Social Media Fraudulent Account Detection",
            "subtitle": "Social Network Security System",
            "description": "A machine learning system for detecting fraudulent accounts on Instagram, Facebook, and Twitter. Analyses user activity patterns, profile data, posting behaviour, and network interactions to classify accounts using Random Forest, Decision Trees, and Logistic Regression.",
            "tech_stack": "Python, Scikit-learn, Pandas, NumPy, Data Mining, Random Forest, Logistic Regression, Decision Tree",
            "live_url": "",
            "github_url": "https://github.com/issahsalim/social-fraud-detection",
            "order": 5
        },
        {
            "title": "Campus Assistant Mobile App",
            "subtitle": "AI-Powered Campus Navigation Tool",
            "description": "Cross-platform mobile application built with Expo React Native addressing campus navigation challenges at UENR. Features GPS-aware campus navigation, Wi-Fi resource discoverability, support contact accessibility, and an AI chat assistant powered by university knowledge data.",
            "tech_stack": "Expo React Native, Django REST API, AI Chat Assistant, GPS Navigation, PostgreSQL, JWT Authentication",
            "live_url": "",
            "github_url": "https://github.com/issahsalim/campus-assistant",
            "order": 6
        },
        {
            "title": "FoodLens / Foodie",
            "subtitle": "AI Food & Recipe Platform",
            "description": "AI-powered food recognition mobile app with recipe generation, voice-enabled meal chat assistant, shopping list management, and video tutorials. Uses a local Swin Transformer model with Gemini generative AI fallback.",
            "tech_stack": "Django REST Framework, Expo React Native, Swin Transformer, Gemini AI, JWT, RapidAPI, YouTube Data API, Expo Router",
            "live_url": "",
            "github_url": "https://github.com/issahsalim/foodlens",
            "order": 7
        },
        {
            "title": "PARL GH — Parliamentary Hansard AI Summarizer",
            "subtitle": "Ghana Parliamentary Intelligence System",
            "description": "Django-based backend for an AI-powered parliamentary hansard summarization system focused on Ghana parliamentary debates. Stores session data, full-text search across speakers/topics, and generates AI summaries for debate segments.",
            "tech_stack": "Django, Django REST Framework, AI Summarization, Full-Text Search, PostgreSQL, JSON/CSV Export",
            "live_url": "",
            "github_url": "https://github.com/issahsalim/parl-gh",
            "order": 8
        },
        {
            "title": "Hospital ID Card Generator",
            "subtitle": "Healthcare Staff Utility",
            "description": "Web-based ID card generator for hospital staff to produce standardized patient ID cards. Features front & back card preview, barcode generation from ID value, and card downloading.",
            "tech_stack": "HTML, CSS, JavaScript, Barcode Generation",
            "live_url": "",
            "github_url": "https://github.com/issahsalim/hospital-id-generator",
            "order": 9
        },
        {
            "title": "RideShare Ghana",
            "subtitle": "Intercity Ride Sharing Platform",
            "description": "Django-based rideshare web application designed for people in Ghana to share intercity rides. Lets users post rides as drivers, search for available rides, book seats, and manage trips with live chatting.",
            "tech_stack": "Django, Python, HTML, CSS, JavaScript, MySQL",
            "live_url": "",
            "github_url": "https://github.com/issahsalim/rideshare-ghana",
            "order": 10
        }
    ]

    for proj in projects_data:
        Project.objects.create(**proj)
    print(f"Seeded {len(projects_data)} projects.")
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed()
