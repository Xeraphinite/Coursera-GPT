import gradio as gr
import openai
import os

os.environ['OPENAI_API_KEY'] = 'YOUR_API_KEY'
openai.api_key = 'YOUR_API_KEY'


def predict(education_level, annual_income, employment_status, course_name, introduction, other_information):
    overall_prompt = '''你将作为一名专业的申请人助手，在世界上最大的 MOOC 平台 Coursera 上完成一份 Financial Aid 相关的任务，任务如下：'''
    role = f'''个人信息： a {education_level} with {annual_income} annual income and {employment_status}.'''

    # 1. Reasons for aid
    task = '请你完成一份 Financial Aid 申请表，字数在 150-300 words 之间，内容需要包括，请注意，输出仅仅包括Reasons for Financial Aid ' \
           'Application 的内容即可，前后均不需要添加任何东西（包括 "Reasons for Financial Aid Application:"），也不需要输出任何解释性语句.'

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        messages=[
            {'role': 'system', 'name': 'overall_prompt', 'content': overall_prompt},
            {'role': 'user', 'name': 'task', 'content': task},
            {'role': 'user', 'name': 'role', 'content': role},
            {'role': 'user', 'name': 'course_name', 'content': f'Course name: {course_name}'},
            {'role': 'user', 'name': 'course_introduction', 'content': f'Course introduction: {introduction}'},
            {'role': 'user', 'name': 'other_information', 'content': f'Other information: {other_information}'},
            {'role': 'system', 'name': 'overall_prompt', 'content': overall_prompt},
            {'role': 'user', 'name': 'task', 'content': task},
        ]
    )

    reasons_for_aid = response.choices[0].message.content
    reasons_for_aid = reasons_for_aid.replace('Reasons for Financial Aid Application:\n', '')
    while reasons_for_aid.startswith('\n'):
        reasons_for_aid = reasons_for_aid[1:]

    # 2. How will your selected course help with your goals?
    task = '请你根据给出的信息回答：How will your selected course help with your goals? 答案字数在 150-300 words ' \
           '之间，请注意，输出仅仅包括问题的答案即可，前后均不需要添加任何东西，也不需要输出任何解释性语句.'

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        temperature=0.5,
        messages=[
            {'role': 'system', 'name': 'overall_prompt', 'content': overall_prompt},
            {'role': 'user', 'name': 'task', 'content': task},
            {'role': 'user', 'name': 'role', 'content': role},
            {'role': 'user', 'name': 'course_name', 'content': f'Course name: {course_name}'},
            {'role': 'user', 'name': 'course_introduction', 'content': f'Course introduction: {introduction}'},
            {'role': 'user', 'name': 'other_information', 'content': f'Other information: {other_information}'},
            {'role': 'system', 'name': 'overall_prompt', 'content': overall_prompt},
            {'role': 'user', 'name': 'task', 'content': task},
        ]
    )

    how_will_course_help = response.choices[0].message.content

    return reasons_for_aid, how_will_course_help


default_params = {
    'course_name': 'Visual Elements of User Interface Design',
    'introduction': '''This design-centric course examines the broad question of what an interface is and what role a 
    designer plays in creating a user interface. Learning how to design and articulate meaning using color, type, 
    and imagery is essential to making interfaces function clearly and seamlessly. Through a series of lectures and 
    visual exercises, you will focus on the many individual elements and components that make up the skillset of an 
    interface designer. By the end of this course, you will be able to describe the key formal elements of clear, 
    consistent, and intuitive UI design, and apply your learned skills to the design of a static screen-based 
    interface. This is the first course in the UI/UX Design Specialization, which brings a design-centric approach to 
    user interface (UI) and user experience (UX) design, and offers practical, skill-based instruction centered 
    around a visual communications perspective, rather than on one focused on marketing or programming alone. These 
    courses are ideal for anyone with some experience in graphic or visual design and who would like to build their 
    skill set in UI or UX for app and web design. It would also be ideal for anyone with experience in front- or 
    back-end web development or human-computer interaction and want to sharpen their visual design and analysis 
    skills for UI or UX.''',
    'other_information': 'I am a student in the University of Melbourne.'
}

if __name__ == '__main__':
    gr.Interface(
        fn=predict,
        inputs=[
            gr.components.Dropdown(['High School', 'Some College', 'College Degree', 'Master’s/Advanced degree', 'Other'], value='College Degree', label='Education'),
            gr.components.Slider(0, 100, 0, label='Annual Income($ USD)'),
            gr.components.Dropdown(['Full-time', 'Part-time', 'Unemployed', 'Student', 'Other'], value='Student', label='Employment Status'),
            gr.inputs.Textbox(lines=1, label="Course Name", default=default_params['course_name']),
            gr.inputs.Textbox(lines=5, label="Introduction", default=default_params['introduction']),
            gr.inputs.Textbox(lines=5, label="Other Information", default=default_params['other_information'])
        ],
        outputs=[
            gr.outputs.Textbox(label="Reason you applied for aid"),
            gr.outputs.Textbox(label="How will your selected course help with your goals?")
        ],
    ).launch(share=True)
