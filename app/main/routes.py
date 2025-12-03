from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    profile_data = {
        "name": "DevOps Engineer",
        "foreword": (
            "I am a DevOps engineer with 3 years of experience, holding a Bachelor's degree "
            "in Electronic and Telecommunication. I am currently pursuing a Master's degree "
            "on Computer Systems and Cybersecurity."
        ),
        "education": [
            {
                "degree": "Master's in Computer Systems and Cybersecurity",
                "status": "In Progress"
            },
            {
                "degree": "Bachelor's in Electronic and Telecommunication",
                "status": "Completed"
            }
        ],
        "repos": [
            {"name": "infrastructure-as-code-lab", "url": "#", "desc": "Terraform and Ansible playground"},
            {"name": "ci-cd-pipelines", "url": "#", "desc": "Jenkins and GitHub Actions workflows"},
            {"name": "flask-blueprint-portfolio", "url": "#", "desc": "Source code for this website"}
        ]
    }   
    return render_template('index.html', **profile_data)