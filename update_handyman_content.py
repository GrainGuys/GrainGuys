#!/usr/bin/env python3
"""Update site copy for GrainGuys handyman services."""
import re
from pathlib import Path

ROOT = Path(__file__).parent

REPLACEMENTS = [
    # Phone
    ('href="tel:+123456789"', 'href="tel:07709034572"'),
    ('href="tel:123456789"', 'href="tel:07709034572"'),
    ('href="tel:+91123456789"', 'href="tel:07709034572"'),
    ('+91 123 456 789', '07709 034572'),
    ('(555) 123-4567', '07709 034572'),
    # Footer & taglines
    (
        "Trusted. Professional. Hassle-free moving solutions. From start to finish, we're here to make it smooth.",
        "Reliable handyman services you can trust. Quality workmanship, fair rates, and friendly service for every home project.",
    ),
    (
        "Trusted. Professional. Hassle-free moving solutions. From start to finish, we're here to\n                                make it smooth.",
        "Reliable handyman services you can trust. Quality workmanship, fair rates, and friendly service for every home project.",
    ),
    ("Subscribe for alerts, our latest blog posts, and moving insights.", "Subscribe for project tips, updates, and handyman insights."),
    ("Subscribe for alerts, our latest blogs, thoughts, and insights.", "Subscribe for project tips, updates, and handyman insights."),
    # CTAs
    ("Get Started", "Free Estimate"),
    ("Request a Quote", "Free Estimate"),
    ("Book Your Service Today", "Get a Free Estimate"),
    ("Contact Us Today", "Request Free Estimate"),
    # Titles
    ("GrainGuys - Moving & Packing Company", "GrainGuys - Handyman Services"),
    # Service names (order matters - specific before general)
    ("Residential Moving", "General Repairs & Maintenance"),
    ("Commercial Moving", "Furniture Assembly"),
    ("Specialty Item Moving", "Painting & Decorating"),
    ("Eco-Friendly Moving", "Flooring & Tiling"),
    ("Office Relocation", "Custom Woodwork"),
    ("Packing & Unpacking", "Shop Counter Construction"),
    ("Storage Solutions", "Bespoke Design Work"),
    ("Moving Assistance", "General Handyman Services"),
    # Service descriptions
    ("Hassle-free home moving services tailored to your needs.", "Repairs, fixes, and upkeep to keep your home in great shape."),
    ("Professional business moving services ensuring efficient, on-time relocations.", "Flat-pack and furniture assembly done right the first time."),
    ("Professional business moving services that ensure efficient, on-time relocations.", "Interior painting with a clean, professional finish."),
    ("Professional handling of fragile and valuable items with safe transport guaranteed.", "Tile, laminate, and flooring installation with precision."),
    ("Expert handling of fragile and valuable items, ensuring safe transport of antiques and heirlooms.", "Shelving, built-ins, and custom storage tailored to your space."),
    ("Sustainable moving solutions using eco-friendly materials and methods to reduce waste.", "Retail and shop counters built to your specifications."),
    ("Sustainable moving solutions using eco-friendly materials and methods to reduce environmental impact.", "One-off jobs and bespoke carpentry for your home or business."),
    # Section headings
    ("Trusted Moving Services <span>Built\n                                Around Your Needs</span>", "Handyman Services <span>Built Around Your Needs</span>"),
    ("Trusted Moving Services <span>Built Around Your Needs</span>", "Handyman Services <span>Built Around Your Needs</span>"),
    ("Setting New Standards in the <span>Moving Industry</span>", "Reliable Handyman Services <span>You Can Trust</span>"),
    ("Setting New Standards in the\n                                <span>Moving Industry</span>", "Reliable Handyman Services <span>You Can Trust</span>"),
    ("Choice for Moving</span>", "Choice for Home Projects</span>"),
    ("Answers to Your <span>Moving Questions</span>", "Answers to Your <span>Handyman Questions</span>"),
    ("Every Move Matters—<span>Explore Our\n                                Recent Work</span>", "Every Project Matters—<span>Explore Our Recent Work</span>"),
    ("Every Move Matters—<span>Explore Our Recent Work</span>", "Every Project Matters—<span>Explore Our Recent Work</span>"),
    # About copy
    (
        "We redefine the moving experience with professionalism, reliability, and exceptional care. By combining innovative solutions, personalized service, and a commitment to excellence, we set new industry standards.",
        "With years of hands-on experience, GrainGuys offers dependable handyman services for homeowners who want jobs done properly, promptly, and professionally.",
    ),
    (
        "We redefine the moving experience with professionalism, reliability, and unmatched care. By combining innovative solutions, personalized service, and a commitment to excellence, we set new benchmarks in the industry.",
        "With years of hands-on experience, GrainGuys offers dependable handyman services for homeowners who want jobs done properly, promptly, and professionally.",
    ),
    ("Helping families and businesses reach their new destinations", "Home projects completed with care and craftsmanship"),
    ("Our customer satisfaction rate speaks for itself", "Customers who recommend our workmanship"),
    # Owner
    ('"Moving is not just about transporting belongings—it is about embracing change and starting fresh. We are committed to making your journey smooth so you can focus on settling into your new beginning."', '"Let\'s get your home projects done — properly, promptly, and professionally. I take pride in quality work, honest pricing, and showing up when I say I will."'),
    ('"Moving is not just about relocating belongings—it is about embracing change and starting fresh. We are committed to making your journey smooth so you can focus on settling into your new beginning."', '"Let\'s get your home projects done — properly, promptly, and professionally. I take pride in quality work, honest pricing, and showing up when I say I will."'),
    ("Savannah Nguyen", "GrainGuys"),
    ("CEO, GrainGuys", "Experienced Handyman"),
    # Why choose
    ("On-time service with no hidden fees.", "Quality workmanship on every job."),
    ("Safe and secure transport for your belongings.", "Fair and honest rates with no surprises."),
    ("Custom moving plans tailored to your needs.", "Reliable, friendly service you can count on."),
    ("Eco-friendly methods for sustainable moving.", "Flexible availability to suit your schedule."),
    # Work process
    ("Get a Quote", "Free Estimate"),
    ("Start by contacting us for a free, personalized quote. Share the details of your move with us.", "Call or text for a free estimate. Tell us about your project and we'll provide honest advice."),
    ("Plan Your Move", "Plan the Job"),
    ("Our team works with you to create a custom moving plan—from packing to logistics.", "We agree on scope, materials, and timing so you know exactly what to expect."),
    ("Safe &amp; Secure Moving", "Quality Work"),
    ("Safe & Secure Moving", "Quality Work"),
    ("Our expert movers handle your belongings with care, using high-quality packing materials.", "Skilled, hands-on work using the right tools and techniques for a lasting finish."),
    ("Unpack &amp; Settle In", "Job Complete"),
    ("Unpack & Settle In", "Job Complete"),
    ("After delivery, we help you unpack and get set up so you can enjoy your new space.", "We tidy up, walk you through the finished work, and make sure you're happy with the result."),
    # Skills
    ("Experienced Movers with a Passion for\n                                <span>Excellence</span>", "Experienced, Skilled &amp; <span>Dependable</span>"),
    ("Experienced Movers with a Passion for <span>Excellence</span>", "Experienced, Skilled & <span>Dependable</span>"),
    ("Our team has the skills and expertise to manage every aspect of your move. From careful packing to attentive transport, we ensure your belongings are handled with precision.", "Looking for a professional you can count on? From repairs and assembly to custom woodwork, I bring years of practical experience to every project."),
    ("Real-Time Tracking", "Carpentry & Woodwork"),
    ("Specialty Handling", "Painting & Decorating"),
    ("Customer-Focused Approach", "General Repairs"),
    # Projects
    ("Urban Home Relocation", "Custom Kitchen Shelving"),
    ("Cityscape Moves", "Built-in Storage Solution"),
    ("Luxury Home Moves", "Flooring & Tiling"),
    ("Smooth Office Relocation", "Shop Counter Build"),
    ("Dream Suburban Moves", "Furniture Assembly"),
    ("Corporate Relocation", "Interior Painting"),
    (
        "Take a closer look at our recent projects and see how we turn every move into a seamless experience. From small local relocations to large-scale moves, we take pride in the care we deliver.",
        "Take a closer look at recent jobs—from quick repairs to bespoke carpentry—and see the care we put into every project.",
    ),
    ("Expert packing for your move. <a href=\"contact.html\">Contact us today</a>", "Free estimates available. <a href=\"contact.html\">Call or text today</a>"),
    # Mission/vision
    ("Our mission is to provide customized, hassle-free moving services with a focus on care and efficiency.", "Our mission is to deliver reliable handyman services with quality workmanship and honest communication."),
    ("Our vision is to redefine the moving experience by prioritizing customer satisfaction and innovative solutions.", "Our vision is to be the handyman homeowners trust for repairs, improvements, and bespoke woodwork."),
    ("Trusted by over 3,500 clients for reliable moves.", "Trusted for reliable, friendly handyman work."),
    ("Our mission is rooted in delivering smooth, stress-free moving experiences tailored to your unique needs, ensuring every step of your move is handled with care, efficiency, and professionalism.", "We deliver stress-free home projects tailored to your needs—handled with care, skill, and professionalism from start to finish."),
    # Contact
    ("Call us for inquiries", "Call or text for a free estimate"),
    ("Visit us anytime", "Serving local homeowners"),
    # Form fields
    ('placeholder="Distance"', 'placeholder="Project Location"'),
    ("data-error=\"Distance is required\"", "data-error=\"Project location is required\""),
    ('<option value="" disabled selected>Move Type</option>', '<option value="" disabled selected>Project Urgency</option>'),
    ('<option value="local">Local Move</option>', '<option value="standard">Standard</option>'),
    ('<option value="long_distance">Long Distance Move</option>', '<option value="urgent">Urgent</option>'),
    ('<option value="international">International Move</option>', '<option value="flexible">Flexible</option>'),
    ('name="movetype"', 'name="urgency"'),
    ("data-error=\"Move type is required\"", "data-error=\"Please select urgency\""),
    ('<option value="residential_moving">General Repairs & Maintenance</option>', '<option value="general_repairs">General Repairs & Maintenance</option>'),
    ('<option value="commercial_moving">Furniture Assembly</option>', '<option value="furniture_assembly">Furniture Assembly</option>'),
    ('<option value="specialty_item">Painting & Decorating</option>', '<option value="painting">Painting & Decorating</option>'),
    ('<option value="eco_friendly">Flooring & Tiling</option>', '<option value="flooring">Flooring & Tiling</option>'),
    ('<option value="office_relocation">Custom Woodwork</option>', '<option value="woodwork">Custom Woodwork</option>'),
    ('<option value="packing_unpacking">Shop Counter Construction</option>', '<option value="shop_counter">Shop Counter Construction</option>'),
    ('<option value="storage_solutions">Bespoke Design Work</option>', '<option value="bespoke">Bespoke Design Work</option>'),
    ('<option value="moving_assistance">General Handyman Services</option>', '<option value="general">General Handyman Services</option>'),
    # Page titles
    ("GrainGuys - Residential Moving", "GrainGuys - General Repairs & Maintenance"),
    ("Moving to an Urban Retreat", "Custom Built-in Storage Project"),
    # Scrolling ticker / misc moving refs
    ("Moving Choice", "GrainGuys Choice"),
    ("Custom moving plans tailored to your needs.", "Custom solutions tailored to your home."),
    ("Eco-friendly methods for sustainable moving.", "Quality materials and proven techniques."),
]

HERO_REPLACEMENTS = [
    (
        """<h1 class="text-anime-style-2" data-cursor="-opaque">A Worry-Free
                                    <span>Moving</span> Experience</h1>
                                <p class="wow fadeInUp">Experts in hassle-free moving</p>""",
        """<h1 class="text-anime-style-2" data-cursor="-opaque">Reliable Handyman
                                    <span>Services</span> You Can Trust</h1>
                                <p class="wow fadeInUp">Experienced – Skilled – Dependable</p>""",
    ),
    (
        "<p>Enjoy a stress-free move with our professional services—from careful packing to smooth transport and on-time delivery.</p>",
        "<p>Looking for a professional you can count on? I offer a full range of handyman services—from repairs and assembly to painting, flooring, and custom woodwork.</p>",
    ),
]


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    original = text
    if path.name in ("index.html", "index-video.html", "index-slider.html"):
        for old, new in HERO_REPLACEMENTS:
            text = text.replace(old, new)
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return 1
    return 0


def main():
    count = 0
    for path in sorted(ROOT.glob("*.html")):
        if process_file(path):
            print(path.name)
            count += 1
    print(f"Updated {count} files")


if __name__ == "__main__":
    main()
