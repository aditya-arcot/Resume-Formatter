# Resume-Formatter

## Description
ATS-compliant resume formatting tool  
Source code written in Python and Tex   
Supported platforms - macOS, Linux  
Requirements - Latexmk  


## Usage
Create text file with contents of resume  
Organize info, format sections and headings as shown below  
Run `python3 generate_resume.py resume_text_file` to generate PDF of resume 


## Resume text file
This tool is configured to work on information provided for the following sections
- Personal
- Objective
- Education
- Coursework
- Technical Skills
- Experience
- Projects


## Section formatting
Each section must begin with -- followed by the section name and end with ====
For example, see the following Objective section: 
```
--Objective
Software engineer looking to continue his career at a dynamic organization
====
```


## Information
Following characters are not supported - ~, ^, \
The information listed for each section is required unless otherwise specified

### Personal
```
Name  
Phone number  
Email   
Website 
```

### Objective
```
Statement 
```

# Education
```
Institution1
Dates
Degree
GPA
Institution2
...
```

### Coursework
```
Course1, Course2, ... 
```

### Technical Skills
```
Category1 - Skill1, Skill2, ...
Category2 - ...
...
```

### Experience
Each title must begin with `-`
Details for each work experience can consist of multiple lines
```
-Title1
Company
Dates
Details1
Details2
...
-Title2
...
```

### Projects
Each name must begin with `-`
Details for each project can consist of multiple lines
```
-Project1
Keywords
Details1
Details2
...
-Project2
...
```




