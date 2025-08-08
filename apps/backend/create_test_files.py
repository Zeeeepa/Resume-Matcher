#!/usr/bin/env python3
"""
Create test files for Resume-Matcher testing
Generates sample PDF and DOCX files for upload testing
"""

import os
import tempfile
from pathlib import Path


def create_sample_resume_html():
    """Create sample resume in HTML format"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Alex Chen - Resume</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #2c3e50; border-bottom: 2px solid #3498db; }
            h2 { color: #34495e; margin-top: 30px; }
            .contact { background: #ecf0f1; padding: 15px; border-radius: 5px; }
            .experience { margin: 20px 0; }
            .skills { display: flex; flex-wrap: wrap; }
            .skill { background: #3498db; color: white; padding: 5px 10px; margin: 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>ALEX CHEN</h1>
        <h2>Full Stack Developer</h2>
        
        <div class="contact">
            <strong>Contact Information</strong><br>
            Email: alex.chen@email.com<br>
            Phone: (555) 987-6543<br>
            LinkedIn: linkedin.com/in/alexchen<br>
            GitHub: github.com/alexchen
        </div>
        
        <h2>Professional Summary</h2>
        <p>Passionate full stack developer with 4 years of experience building modern web applications. 
        Skilled in React, Node.js, and cloud technologies. Strong problem-solving abilities and 
        collaborative team player with a track record of delivering high-quality software solutions.</p>
        
        <h2>Technical Skills</h2>
        <div class="skills">
            <span class="skill">JavaScript (ES6+)</span>
            <span class="skill">TypeScript</span>
            <span class="skill">React</span>
            <span class="skill">Node.js</span>
            <span class="skill">Express</span>
            <span class="skill">Python</span>
            <span class="skill">Django</span>
            <span class="skill">PostgreSQL</span>
            <span class="skill">MongoDB</span>
            <span class="skill">Redis</span>
            <span class="skill">AWS</span>
            <span class="skill">Docker</span>
            <span class="skill">Kubernetes</span>
            <span class="skill">Git</span>
            <span class="skill">Jenkins</span>
        </div>
        
        <h2>Professional Experience</h2>
        
        <div class="experience">
            <h3>Full Stack Developer | WebTech Solutions | 2020 - Present</h3>
            <ul>
                <li>Developed responsive web applications using React and Node.js serving 25K+ daily active users</li>
                <li>Built and maintained RESTful APIs with Express.js and PostgreSQL database</li>
                <li>Implemented automated testing with Jest and Cypress, achieving 90% code coverage</li>
                <li>Collaborated with design team to create intuitive user interfaces and improve UX</li>
                <li>Optimized application performance resulting in 40% faster page load times</li>
                <li>Led migration from monolithic to microservices architecture using Docker</li>
            </ul>
        </div>
        
        <div class="experience">
            <h3>Software Developer | StartupHub | 2019 - 2020</h3>
            <ul>
                <li>Created dynamic websites using JavaScript, PHP, and MySQL</li>
                <li>Optimized database queries improving application performance by 30%</li>
                <li>Participated in agile development process with daily standups and sprint planning</li>
                <li>Implemented responsive design principles for mobile-first development</li>
                <li>Collaborated with cross-functional teams to deliver features on time</li>
            </ul>
        </div>
        
        <div class="experience">
            <h3>Junior Developer | CodeCraft | 2018 - 2019</h3>
            <ul>
                <li>Developed web applications using HTML, CSS, JavaScript, and jQuery</li>
                <li>Maintained legacy systems and performed bug fixes</li>
                <li>Learned modern development practices and version control with Git</li>
                <li>Participated in code reviews and pair programming sessions</li>
            </ul>
        </div>
        
        <h2>Education</h2>
        <div class="experience">
            <h3>Bachelor of Computer Science</h3>
            <p>Tech University | 2018<br>
            Relevant Coursework: Data Structures, Algorithms, Database Systems, Web Development</p>
        </div>
        
        <h2>Notable Projects</h2>
        <div class="experience">
            <h3>E-commerce Platform</h3>
            <p>Built full-stack e-commerce application with React frontend, Node.js backend, and PostgreSQL database. 
            Implemented features including user authentication, payment processing, and inventory management.</p>
            
            <h3>Task Management App</h3>
            <p>Developed mobile-responsive task management web application with real-time updates using WebSocket. 
            Features include drag-and-drop interface, team collaboration, and progress tracking.</p>
            
            <h3>API Gateway Service</h3>
            <p>Created microservices architecture with Docker containers and Kubernetes orchestration. 
            Implemented API gateway with rate limiting, authentication, and load balancing.</p>
        </div>
        
        <h2>Certifications</h2>
        <ul>
            <li>AWS Certified Developer - Associate</li>
            <li>MongoDB Certified Developer</li>
            <li>Certified Scrum Master (CSM)</li>
        </ul>
    </body>
    </html>
    """


def create_sample_job_html():
    """Create sample job description in HTML format"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Senior React Developer - Job Description</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #2c3e50; border-bottom: 2px solid #e74c3c; }
            h2 { color: #34495e; margin-top: 30px; }
            .company { background: #ecf0f1; padding: 15px; border-radius: 5px; }
            .requirements { background: #f8f9fa; padding: 20px; border-left: 4px solid #e74c3c; }
            .benefits { background: #e8f5e8; padding: 20px; border-left: 4px solid #27ae60; }
            ul li { margin: 8px 0; }
        </style>
    </head>
    <body>
        <h1>SENIOR REACT DEVELOPER</h1>
        
        <div class="company">
            <strong>TechInnovate Inc.</strong><br>
            Location: San Francisco, CA (Remote-friendly)<br>
            Department: Frontend Engineering<br>
            Employment Type: Full-time
        </div>
        
        <h2>Position Overview</h2>
        <p>We're looking for a Senior React Developer to join our frontend team and help build the next generation 
        of our web applications. You'll be responsible for creating cutting-edge user interfaces, working closely 
        with our design and backend teams, and mentoring junior developers. This is an excellent opportunity to 
        work with modern technologies and make a significant impact on our product.</p>
        
        <h2>Key Responsibilities</h2>
        <ul>
            <li>Develop complex React applications with modern JavaScript (ES6+) and TypeScript</li>
            <li>Implement responsive designs and ensure cross-browser compatibility</li>
            <li>Collaborate with UX/UI designers to translate mockups into interactive interfaces</li>
            <li>Work with backend developers to integrate APIs and optimize data flow</li>
            <li>Write clean, maintainable, and well-tested code following best practices</li>
            <li>Mentor junior developers and conduct thorough code reviews</li>
            <li>Optimize applications for maximum speed and scalability</li>
            <li>Participate in architectural decisions and technical planning</li>
            <li>Stay up-to-date with latest React ecosystem and frontend trends</li>
        </ul>
        
        <div class="requirements">
            <h2>Required Qualifications</h2>
            <ul>
                <li><strong>5+ years of experience</strong> with React and modern JavaScript development</li>
                <li><strong>Strong proficiency in TypeScript</strong> and modern ES6+ features</li>
                <li><strong>Experience with state management</strong> libraries (Redux, Context API, Zustand)</li>
                <li><strong>Knowledge of modern build tools</strong> (Webpack, Vite, Rollup)</li>
                <li><strong>Familiarity with testing frameworks</strong> (Jest, React Testing Library, Cypress)</li>
                <li><strong>Experience with RESTful APIs</strong> and asynchronous programming</li>
                <li><strong>Understanding of responsive design</strong> principles and CSS preprocessors</li>
                <li><strong>Proficiency with version control</strong> (Git) and collaborative development</li>
                <li><strong>Strong problem-solving skills</strong> and attention to detail</li>
                <li><strong>Excellent communication skills</strong> and ability to work in a team environment</li>
            </ul>
        </div>
        
        <h2>Preferred Qualifications</h2>
        <ul>
            <li>Experience with <strong>Next.js</strong> or other React frameworks</li>
            <li>Knowledge of <strong>GraphQL</strong> and Apollo Client</li>
            <li>Familiarity with <strong>Node.js</strong> and backend development</li>
            <li>Experience with <strong>cloud platforms</strong> (AWS, Azure, GCP)</li>
            <li>Knowledge of <strong>CI/CD pipelines</strong> and DevOps practices</li>
            <li>Experience with <strong>Docker</strong> and containerization</li>
            <li>Familiarity with <strong>microservices architecture</strong></li>
            <li>Contributions to <strong>open-source projects</strong></li>
            <li>Experience with <strong>performance optimization</strong> and monitoring tools</li>
            <li>Knowledge of <strong>accessibility standards</strong> (WCAG)</li>
        </ul>
        
        <h2>Technical Stack</h2>
        <ul>
            <li><strong>Frontend:</strong> React 18, TypeScript, Next.js, Tailwind CSS</li>
            <li><strong>State Management:</strong> Redux Toolkit, React Query</li>
            <li><strong>Testing:</strong> Jest, React Testing Library, Playwright</li>
            <li><strong>Build Tools:</strong> Vite, ESLint, Prettier</li>
            <li><strong>Backend:</strong> Node.js, GraphQL, PostgreSQL</li>
            <li><strong>Infrastructure:</strong> AWS, Docker, Kubernetes</li>
            <li><strong>Monitoring:</strong> DataDog, Sentry</li>
        </ul>
        
        <div class="benefits">
            <h2>What We Offer</h2>
            <ul>
                <li><strong>Competitive salary</strong> ($120,000 - $180,000) plus equity package</li>
                <li><strong>Comprehensive health benefits</strong> (medical, dental, vision)</li>
                <li><strong>Flexible work arrangements</strong> with remote-friendly culture</li>
                <li><strong>Professional development budget</strong> ($3,000/year) for conferences and courses</li>
                <li><strong>Modern tech stack</strong> and cutting-edge development tools</li>
                <li><strong>Collaborative team environment</strong> with experienced engineers</li>
                <li><strong>Unlimited PTO</strong> and flexible working hours</li>
                <li><strong>Stock options</strong> with high growth potential</li>
                <li><strong>Home office stipend</strong> for remote work setup</li>
                <li><strong>Team building events</strong> and company retreats</li>
            </ul>
        </div>
        
        <h2>About TechInnovate Inc.</h2>
        <p>TechInnovate Inc. is a fast-growing technology company focused on building innovative web applications 
        that solve real-world problems. We're backed by top-tier investors and have a strong track record of 
        delivering high-quality products. Our team values collaboration, continuous learning, and technical excellence.</p>
        
        <h2>Application Process</h2>
        <p>To apply, please submit your resume along with a cover letter explaining why you're interested in this 
        position. We'd also love to see examples of your work, whether through a portfolio, GitHub profile, or 
        links to applications you've built.</p>
        
        <p><em>TechInnovate Inc. is an equal opportunity employer committed to diversity and inclusion.</em></p>
    </body>
    </html>
    """


def html_to_text(html_content):
    """Convert HTML to plain text"""
    import re
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_content)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


def create_test_files():
    """Create test files for upload testing"""
    print("📄 Creating test files for Resume-Matcher...")
    
    # Create test directory
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    # Create resume files
    resume_html = create_sample_resume_html()
    resume_text = html_to_text(resume_html)
    
    # Create job description files
    job_html = create_sample_job_html()
    job_text = html_to_text(job_html)
    
    # Save HTML files
    with open(test_dir / "sample_resume.html", "w", encoding="utf-8") as f:
        f.write(resume_html)
    
    with open(test_dir / "sample_job.html", "w", encoding="utf-8") as f:
        f.write(job_html)
    
    # Save text files
    with open(test_dir / "sample_resume.txt", "w", encoding="utf-8") as f:
        f.write(resume_text)
    
    with open(test_dir / "sample_job.txt", "w", encoding="utf-8") as f:
        f.write(job_text)
    
    print(f"✅ Created test files in {test_dir}:")
    print("   • sample_resume.html")
    print("   • sample_resume.txt")
    print("   • sample_job.html")
    print("   • sample_job.txt")
    
    # Try to create PDF files if possible
    try:
        create_pdf_files(test_dir, resume_html, job_html)
    except Exception as e:
        print(f"⚠️  Could not create PDF files: {e}")
        print("   HTML and text files are available for testing")
    
    print("\n📖 Usage:")
    print("   These files can be used to test the Resume-Matcher application.")
    print("   For API testing, you'll need PDF or DOCX files.")
    print("   For direct testing, you can use the text content in your code.")


def create_pdf_files(test_dir, resume_html, job_html):
    """Try to create PDF files using available libraries"""
    try:
        # Try using weasyprint
        import weasyprint
        
        # Create resume PDF
        weasyprint.HTML(string=resume_html).write_pdf(test_dir / "sample_resume.pdf")
        weasyprint.HTML(string=job_html).write_pdf(test_dir / "sample_job.pdf")
        
        print("   • sample_resume.pdf")
        print("   • sample_job.pdf")
        
    except ImportError:
        try:
            # Try using pdfkit
            import pdfkit
            
            pdfkit.from_string(resume_html, test_dir / "sample_resume.pdf")
            pdfkit.from_string(job_html, test_dir / "sample_job.pdf")
            
            print("   • sample_resume.pdf")
            print("   • sample_job.pdf")
            
        except ImportError:
            raise Exception("No PDF library available (weasyprint or pdfkit)")


if __name__ == "__main__":
    create_test_files()

