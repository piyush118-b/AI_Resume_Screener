import fitz
doc = fitz.open()
page = doc.new_page()
page.insert_text(fitz.Point(50, 50), "John Doe\nExperienced Software Engineer\nSkills: Python, Java, Spring Boot, Machine Learning, Docker, SQL\nEducation: Bachelor of Science in Computer Engineering\nI have built multiple AI models and web applications.", fontsize=12)
doc.save("test_resume.pdf")
