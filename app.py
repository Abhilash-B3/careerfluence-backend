from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import io
import base64
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# Ensure charts directory exists
os.makedirs('charts', exist_ok=True)

# Sample data
STREAMS_DATA = {
    'bipc': {
        'id': 'bipc',
        'name': 'BiPC',
        'full_name': 'Biology, Physics, Chemistry',
        'description': 'Perfect for aspiring medical professionals and life science enthusiasts',
        'icon': 'microscope',
        'color': 'green',
        'popular_courses': ['MBBS', 'BDS', 'BAMS', '+2 more'],
        'stats': {
            'popular_courses': 6,
            'entrance_exams': 2,
            'career_options': 3,
            'avg_salary': '₹8-12 LPA'
        }
    },
    'mpc': {
        'id': 'mpc',
        'name': 'MPC',
        'full_name': 'Mathematics, Physics, Chemistry',
        'description': 'Ideal for engineering and scientific research careers',
        'icon': 'calculator',
        'color': 'blue',
        'popular_courses': ['B.Tech', 'B.Sc Physics', 'B.Arch', '+1 more'],
        'stats': {
            'popular_courses': 6,
            'entrance_exams': 3,
            'career_options': 4,
            'avg_salary': '₹6-10 LPA'
        }
    },
    'cec': {
        'id': 'cec',
        'name': 'CEC',
        'full_name': 'Commerce, Economics, Civics',
        'description': 'Gateway to business, finance, and commerce careers',
        'icon': 'trending-up',
        'color': 'purple',
        'popular_courses': ['B.Com', 'BBA', 'CA', '+2 more'],
        'stats': {
            'popular_courses': 6,
            'entrance_exams': 2,
            'career_options': 4,
            'avg_salary': '₹5-8 LPA'
        }
    },
    'diploma': {
        'id': 'diploma',
        'name': 'Diploma',
        'full_name': 'Technical Diploma Courses',
        'description': 'Hands-on technical skills for immediate career opportunities',
        'icon': 'wrench',
        'color': 'orange',
        'popular_courses': ['Civil', 'Mechanical', 'Electrical', '+1 more'],
        'stats': {
            'popular_courses': 6,
            'entrance_exams': 2,
            'career_options': 4,
            'avg_salary': '₹4-7 LPA'
        }
    }
}

COURSES_DATA = {
    'bipc': [
        {'name': 'MBBS', 'full_name': 'Bachelor of Medicine and Bachelor of Surgery', 'duration': '5.5 years', 'avg_fee': '₹10-60 LPA', 'demand': 'Very High'},
        {'name': 'BDS', 'full_name': 'Bachelor of Dental Surgery', 'duration': '5 years', 'avg_fee': '₹2-25 LPA', 'demand': 'High'},
        {'name': 'BAMS', 'full_name': 'Bachelor of Ayurvedic Medicine and Surgery', 'duration': '5.5 years', 'avg_fee': '₹2-10 LPA', 'demand': 'Medium'},
        {'name': 'B.Pharmacy', 'full_name': 'Bachelor of Pharmacy', 'duration': '4 years', 'avg_fee': '₹2-8 LPA', 'demand': 'High'},
        {'name': 'B.Sc Nursing', 'full_name': 'Bachelor of Science in Nursing', 'duration': '4 years', 'avg_fee': '₹1-5 LPA', 'demand': 'Very High'},
        {'name': 'Physiotherapy', 'full_name': 'Bachelor of Physiotherapy', 'duration': '4.5 years', 'avg_fee': '₹2-12 LPA', 'demand': 'High'}
    ],
    'mpc': [
        {'name': 'B.Tech', 'full_name': 'Bachelor of Technology', 'duration': '4 years', 'avg_fee': '₹2-15 LPA', 'demand': 'Very High'},
        {'name': 'B.Sc Physics', 'full_name': 'Bachelor of Science in Physics', 'duration': '3 years', 'avg_fee': '₹50K-2 LPA', 'demand': 'Medium'},
        {'name': 'B.Arch', 'full_name': 'Bachelor of Architecture', 'duration': '5 years', 'avg_fee': '₹2-10 LPA', 'demand': 'High'},
        {'name': 'B.Sc Mathematics', 'full_name': 'Bachelor of Science in Mathematics', 'duration': '3 years', 'avg_fee': '₹30K-1.5 LPA', 'demand': 'Medium'},
        {'name': 'Aerospace Engineering', 'full_name': 'Bachelor in Aerospace Engineering', 'duration': '4 years', 'avg_fee': '₹3-18 LPA', 'demand': 'High'},
        {'name': 'Data Science', 'full_name': 'Bachelor in Data Science', 'duration': '3-4 years', 'avg_fee': '₹2-12 LPA', 'demand': 'Very High'}
    ],
    'cec': [
        {'name': 'B.Com', 'full_name': 'Bachelor of Commerce', 'duration': '3 years', 'avg_fee': '₹30K-2 LPA', 'demand': 'High'},
        {'name': 'BBA', 'full_name': 'Bachelor of Business Administration', 'duration': '3 years', 'avg_fee': '₹1-8 LPA', 'demand': 'High'},
        {'name': 'CA', 'full_name': 'Chartered Accountant', 'duration': '4-5 years', 'avg_fee': '₹2-5 LPA', 'demand': 'Very High'},
        {'name': 'Economics Honors', 'full_name': 'Bachelor in Economics', 'duration': '3 years', 'avg_fee': '₹50K-3 LPA', 'demand': 'Medium'},
        {'name': 'Hotel Management', 'full_name': 'Bachelor in Hotel Management', 'duration': '3-4 years', 'avg_fee': '₹2-8 LPA', 'demand': 'Medium'},
        {'name': 'Digital Marketing', 'full_name': 'Bachelor in Digital Marketing', 'duration': '3 years', 'avg_fee': '₹1-5 LPA', 'demand': 'High'}
    ],
    'diploma': [
        {'name': 'Civil Engineering', 'full_name': 'Diploma in Civil Engineering', 'duration': '3 years', 'avg_fee': '₹50K-2 LPA', 'demand': 'High'},
        {'name': 'Mechanical Engineering', 'full_name': 'Diploma in Mechanical Engineering', 'duration': '3 years', 'avg_fee': '₹50K-2 LPA', 'demand': 'High'},
        {'name': 'Electrical Engineering', 'full_name': 'Diploma in Electrical Engineering', 'duration': '3 years', 'avg_fee': '₹50K-2 LPA', 'demand': 'High'},
        {'name': 'Computer Science', 'full_name': 'Diploma in Computer Science', 'duration': '3 years', 'avg_fee': '₹1-3 LPA', 'demand': 'Very High'},
        {'name': 'Electronics', 'full_name': 'Diploma in Electronics Engineering', 'duration': '3 years', 'avg_fee': '₹50K-2 LPA', 'demand': 'Medium'},
        {'name': 'Automobile Engineering', 'full_name': 'Diploma in Automobile Engineering', 'duration': '3 years', 'avg_fee': '₹1-2.5 LPA', 'demand': 'Medium'}
    ]
}

JOBS_EXAMS_DATA = {
    'bipc': {
        'jobs': [
            {'title': 'Medical Doctor', 'description': 'Practice medicine and treat patients', 'salary_range': '₹8-50 LPA', 'growth': 'Very High', 'skills': ['Medical Knowledge', 'Patient Care', 'Diagnosis']},
            {'title': 'Research Scientist', 'description': 'Conduct biological and medical research', 'salary_range': '₹6-25 LPA', 'growth': 'High', 'skills': ['Research', 'Lab Skills', 'Data Analysis']},
            {'title': 'Pharmacist', 'description': 'Dispense medications and provide pharmaceutical care', 'salary_range': '₹4-15 LPA', 'growth': 'Medium', 'skills': ['Pharmacy Knowledge', 'Patient Counseling', 'Quality Control']},
            {'title': 'Biotechnologist', 'description': 'Apply biological processes in technology and industry', 'salary_range': '₹5-20 LPA', 'growth': 'High', 'skills': ['Biotechnology', 'Lab Techniques', 'Innovation']}
        ],
        'exams': [
            {'name': 'NEET', 'full_name': 'National Eligibility cum Entrance Test for medical courses', 'difficulty': 'High', 'for_courses': 'MBBS, BDS, BAMS', 'exam_date': 'May 2025', 'application': 'December 2024 - January 2025'},
            {'name': 'AIIMS', 'full_name': 'All India Institute of Medical Sciences Entrance', 'difficulty': 'Very High', 'for_courses': 'MBBS', 'exam_date': 'May 2025', 'application': 'February - March 2025'}
        ]
    },
    'mpc': [
        {'title': 'Software Engineer', 'description': 'Develop and maintain software applications', 'salary_range': '₹6-30 LPA', 'growth': 'Very High', 'skills': ['Programming', 'Problem Solving', 'Algorithms']},
        {'title': 'Mechanical Engineer', 'description': 'Design and develop mechanical systems', 'salary_range': '₹4-18 LPA', 'growth': 'Medium', 'skills': ['CAD', 'Manufacturing', 'Thermodynamics']},
        {'title': 'Data Scientist', 'description': 'Analyze complex data to drive business decisions', 'salary_range': '₹8-35 LPA', 'growth': 'Very High', 'skills': ['Statistics', 'Python', 'Machine Learning']},
        {'title': 'Aerospace Engineer', 'description': 'Design aircraft and spacecraft systems', 'salary_range': '₹6-25 LPA', 'growth': 'High', 'skills': ['Aerodynamics', 'Materials', 'CAD']}
    ],
    'exams': [
        {'name': 'JEE Main', 'full_name': 'Joint Entrance Examination for engineering courses', 'difficulty': 'High', 'for_courses': 'B.Tech', 'exam_date': 'January & April 2025', 'application': 'November 2024 - December 2024'},
        {'name': 'JEE Advanced', 'full_name': 'For admission to IITs', 'difficulty': 'Very High', 'for_courses': 'B.Tech at IITs', 'exam_date': 'May 2025', 'application': 'After JEE Main results'},
        {'name': 'BITSAT', 'full_name': 'Birla Institute of Technology and Science Admission Test', 'difficulty': 'High', 'for_courses': 'B.Tech at BITS', 'exam_date': 'May 2025', 'application': 'January - March 2025'}
    ]
}

GOV_JOBS_DATA = [
    {
        'id': 1,
        'title': 'Civil Services Examination',
        'organization': 'UPSC',
        'category': 'UPSC',
        'status': 'Open',
        'description': 'Recruitment for IAS, IPS, IFS and other Group A services',
        'vacancies': 861,
        'location': 'Pan India',
        'qualification': 'Graduate from recognized university',
        'salary': '₹56,100 - ₹2,50,000',
        'age_limit': '21-32 years',
        'apply_by': '31st March 2025',
        'exam_dates': {
            'prelims': 'June 2025',
            'mains': 'October 2025'
        },
        'apply_link': 'https://upsc.gov.in'
    },
    {
        'id': 2,
        'title': 'SSC Combined Graduate Level',
        'organization': 'Staff Selection Commission',
        'category': 'SSC',
        'status': 'Open',
        'description': 'Recruitment for Group B and C posts in various ministries',
        'vacancies': 3261,
        'location': 'Various States',
        'qualification': 'Bachelor degree from recognized university',
        'salary': '₹25,500 - ₹81,100',
        'age_limit': '18-27 years',
        'apply_by': '15th February 2025',
        'exam_dates': {
            'tier1': 'April 2025',
            'tier2': 'June 2025'
        },
        'apply_link': 'https://ssc.nic.in'
    },
    {
        'id': 3,
        'title': 'SBI Probationary Officer',
        'organization': 'State Bank of India',
        'category': 'Banking',
        'status': 'Open',
        'description': 'Recruitment for Probationary Officer positions',
        'vacancies': 2000,
        'location': 'Pan India',
        'qualification': 'Graduate in any discipline',
        'salary': '₹27,620 - ₹50,000',
        'age_limit': '21-30 years',
        'apply_by': '20th March 2025',
        'exam_dates': {
            'prelims': 'May 2025',
            'mains': 'July 2025'
        },
        'apply_link': 'https://sbi.co.in/careers'
    },
    {
        'id': 4,
        'title': 'Railway Recruitment Board NTPC',
        'organization': 'Indian Railways',
        'category': 'Railways',
        'status': 'Closing Soon',
        'description': 'Non-Technical Popular Categories recruitment',
        'vacancies': 35281,
        'location': 'Pan India',
        'qualification': 'Graduate/Undergraduate as per post',
        'salary': '₹19,900 - ₹63,200',
        'age_limit': '18-33 years',
        'apply_by': '31st January 2025',
        'exam_dates': {
            'cbt1': 'March 2025',
            'cbt2': 'May 2025'
        },
        'apply_link': 'https://indianrailways.gov.in'
    },
    {
        'id': 5,
        'title': 'Indian Army Technical Entry Scheme',
        'organization': 'Indian Army',
        'category': 'Defense',
        'status': 'Open',
        'description': 'Direct entry for Engineering graduates',
        'vacancies': 40,
        'location': 'Various Cantonments',
        'qualification': 'BE/B.Tech in specified branches',
        'salary': '₹56,100 - ₹1,77,500',
        'age_limit': '20-27 years',
        'apply_by': '28th February 2025',
        'exam_dates': {
            'ssb': 'April-June 2025'
        },
        'apply_link': 'https://indianarmy.nic.in'
    },
    {
        'id': 6,
        'title': 'Andhra Pradesh Public Service Commission',
        'organization': 'APPSC',
        'category': 'State PSC',
        'status': 'Open',
        'description': 'Group I Services recruitment',
        'vacancies': 503,
        'location': 'Andhra Pradesh',
        'qualification': 'Graduate from recognized university',
        'salary': '₹36,400 - ₹1,16,600',
        'age_limit': '21-42 years',
        'apply_by': '15th March 2025',
        'exam_dates': {
            'prelims': 'May 2025',
            'mains': 'August 2025'
        },
        'apply_link': 'https://psc.ap.gov.in'
    }
]

def create_stream_popularity_chart():
    """Create and save stream popularity pie chart"""
    streams = ['MPC', 'BiPC', 'CEC', 'Diploma']
    popularity = [45, 30, 15, 10]
    colors = ['#3B82F6', '#10B981', '#8B5CF6', '#F97316']
    
    plt.figure(figsize=(10, 8))
    wedges, texts, autotexts = plt.pie(popularity, labels=streams, colors=colors, 
                                       autopct='%1.1f%%', startangle=90, 
                                       textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    # Enhance the appearance
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.title('Stream Popularity Distribution (Out of 100 Students)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('charts/stream_popularity.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()

def create_emerging_trends_chart():
    """Create and save emerging trends bar chart"""
    fields = ['Data Science', 'Digital Marketing', 'Cybersecurity', 'Healthcare', 'Renewable Energy', 'AI/ML']
    growth = [45, 38, 42, 25, 35, 50]
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(fields, growth, color=['#3B82F6', '#10B981', '#8B5CF6', '#F97316', '#06B6D4', '#EF4444'])
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'+{height}%', ha='center', va='bottom', fontweight='bold')
    
    plt.title('Emerging Career Trends - Growth Rate (%)', fontsize=16, fontweight='bold')
    plt.xlabel('Career Fields', fontsize=12, fontweight='bold')
    plt.ylabel('Growth Rate (%)', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('charts/emerging_trends.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

def create_salary_trends_chart():
    """Create and save salary trends line chart"""
    years = [2020, 2021, 2022, 2023, 2024]
    mpc_salaries = [5.2, 5.8, 6.5, 7.2, 8.0]
    bipc_salaries = [6.0, 6.8, 7.5, 8.2, 9.0]
    cec_salaries = [4.5, 5.0, 5.5, 6.0, 6.5]
    diploma_salaries = [3.8, 4.2, 4.6, 5.0, 5.5]
    
    plt.figure(figsize=(12, 8))
    plt.plot(years, mpc_salaries, marker='o', linewidth=3, label='MPC', color='#3B82F6')
    plt.plot(years, bipc_salaries, marker='s', linewidth=3, label='BiPC', color='#10B981')
    plt.plot(years, cec_salaries, marker='^', linewidth=3, label='CEC', color='#8B5CF6')
    plt.plot(years, diploma_salaries, marker='d', linewidth=3, label='Diploma', color='#F97316')
    
    plt.title('Average Starting Salary Trends by Stream', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12, fontweight='bold')
    plt.ylabel('Average Salary (LPA)', fontsize=12, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('charts/salary_trends.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

def create_demand_skills_chart():
    """Create and save in-demand skills horizontal bar chart"""
    skills = ['Python', 'Data Analysis', 'Digital Marketing', 'Communication', 'Problem Solving', 
              'Machine Learning', 'Project Management', 'Cloud Computing']
    demand_score = [95, 88, 82, 90, 92, 85, 78, 80]
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(skills, demand_score, color='#3B82F6')
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 1, bar.get_y() + bar.get_height()/2, 
                f'{demand_score[i]}%', ha='left', va='center', fontweight='bold')
    
    plt.title('Most In-Demand Skills in 2024', fontsize=16, fontweight='bold')
    plt.xlabel('Demand Score (%)', fontsize=12, fontweight='bold')
    plt.xlim(0, 100)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('charts/demand_skills.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

# Generate all charts on startup
create_stream_popularity_chart()
create_emerging_trends_chart()
create_salary_trends_chart()
create_demand_skills_chart()

# API Routes

@app.route('/api/streams', methods=['GET'])
def get_streams():
    """Get all streams"""
    return jsonify(list(STREAMS_DATA.values()))

@app.route('/api/streams/<stream_id>', methods=['GET'])
def get_stream(stream_id):
    """Get specific stream details"""
    if stream_id in STREAMS_DATA:
        return jsonify(STREAMS_DATA[stream_id])
    return jsonify({'error': 'Stream not found'}), 404

@app.route('/api/streams/<stream_id>/courses', methods=['GET'])
def get_courses(stream_id):
    """Get courses for a specific stream"""
    if stream_id in COURSES_DATA:
        return jsonify(COURSES_DATA[stream_id])
    return jsonify([])

@app.route('/api/streams/<stream_id>/jobs', methods=['GET'])
def get_jobs(stream_id):
    """Get jobs and exams for a specific stream"""
    if stream_id in JOBS_EXAMS_DATA:
        return jsonify(JOBS_EXAMS_DATA[stream_id])
    return jsonify({'jobs': [], 'exams': []})

@app.route('/api/gov-jobs', methods=['GET'])
def get_gov_jobs():
    """Get government jobs"""
    return jsonify(GOV_JOBS_DATA)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overview statistics"""
    return jsonify({
        'studentsGuided': 10000,
        'careerPaths': 500,
        'successRate': 95
    })

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data"""
    year = request.args.get('year', '2024')
    return jsonify({
        'overview_stats': {
            'total_jobs': 2500000,
            'new_opportunities': 450000,
            'average_package': 6.5,
            'placement_rate': 78
        },
        'emerging_trends': [
            {'field': 'Data Science', 'growth': 45, 'demand': 'Very High', 'avg_salary': '₹12-25 LPA'},
            {'field': 'Digital Marketing', 'growth': 38, 'demand': 'High', 'avg_salary': '₹6-15 LPA'},
            {'field': 'Cybersecurity', 'growth': 42, 'demand': 'Very High', 'avg_salary': '₹10-30 LPA'},
            {'field': 'Healthcare', 'growth': 25, 'demand': 'High', 'avg_salary': '₹8-20 LPA'},
            {'field': 'Renewable Energy', 'growth': 35, 'demand': 'High', 'avg_salary': '₹7-18 LPA'},
            {'field': 'AI/Machine Learning', 'growth': 50, 'demand': 'Very High', 'avg_salary': '₹15-40 LPA'}
        ],
        'stream_popularity_chart': '/api/charts/stream_popularity.png',
        'trends_chart': '/api/charts/emerging_trends.png',
        'salary_trends_chart': '/api/charts/salary_trends.png',
        'demand_skills_chart': '/api/charts/demand_skills.png'
    })

@app.route('/api/charts/<chart_name>', methods=['GET'])
def get_chart(chart_name):
    """Serve chart images"""
    chart_path = f'charts/{chart_name}'
    if os.path.exists(chart_path):
        return send_file(chart_path, mimetype='image/png')
    return jsonify({'error': 'Chart not found'}), 404

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'CareerFluence API is running'})

if __name__ == '__main__':
    print("Starting CareerFluence Backend Server...")
    print("Generating charts...")
    print("Server is ready!")
    app.run(debug=True, host='0.0.0.0', port=8000)