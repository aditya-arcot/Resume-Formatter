'''Generate resume PDF from text file using Latexmk and custom cls file'''

import sys
import os

SLASH = '\\'

def read_input():
    '''read resume info from text file'''

    if len(sys.argv) < 2:
        print('usage: python3 generate_resume.py text_file')
        sys.exit(0)

    infile = sys.argv[1]
    if not os.path.isfile(infile):
        print('file does not exist')
        sys.exit(0)

    path = os.path.dirname(os.path.realpath(infile))

    with open(infile, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    return lines, path


special = ['&', '%', '$', '#', '_', '{', '}']
def replace_special(line):
    '''add backslash to TeX special characters'''

    for i in special:
        line = line.replace(i, SLASH + i)
    return line


def parse_input(lines):
    '''extract 1 section at a time for TeX formatting'''

    out = SLASH + 'documentclass{resume}'
    out += SLASH + 'begin{document}'
    while lines:
        curr = lines.pop(0).strip()
        if not curr.startswith('--'): # skip until next section start
            continue

        section = ''.join(curr.split('--')).strip()
        details = []

        curr = replace_special(lines.pop(0).strip())
        while curr != '====': # until end of section
            if curr: # omit blank lines
                details.append(curr)
            curr = replace_special(lines.pop(0).strip())

        out += format_info(section, details)

    return out + SLASH + 'end{document}'


def check_num_fields(section, lst, num, mode='s'):
    '''check if incorrect number of info fields for a section / entry'''

    if not len(lst) == num:
        msg = f'{section}' + 'section' if mode =='s' else 'entries' + 'must have {n} detail(s)'
        raise Exception(msg)


def format_args(details):
    '''add open and close brackets to args and join together'''

    out = ''
    for i in details:
        out += '{' + i + '}'
    return out


def section_name(section):
    '''add slash and brackets to section name'''

    return SLASH + f'section{{{section}}}'


PERSONAL_INFO_ENTRY = SLASH + 'personalInfoEntry'
TEXT_ENTRY = SLASH + 'textEntry'
TECHNICAL_ENTRY = SLASH + 'technicalEntry'
EDUCATION_ENTRY = SLASH + 'educationEntry'
EXPERIENCE_ENTRY = SLASH + 'experienceEntry'
PROJECT_ENTRY = SLASH + 'projectEntry'
BULLETED_DETAILS = SLASH + 'bulletedDetails'
SPACER = SLASH + 'spacer'

def format_info(section, details):
    '''create TeX formatted section with corresponding details'''

    first_entry = True

    if section == 'Personal':
        check_num_fields(section, details, 4)
        return PERSONAL_INFO_ENTRY + format_args(details)

    if section in ('Objective', 'Coursework'):
        check_num_fields(section, details, 1)
        return section_name(section) + TEXT_ENTRY + format_args(details)

    if section == 'Technical Skills':
        out = section_name(section) + TEXT_ENTRY + '{'
        for i in details:
            split = i.split('-')
            skill_type = split[0].strip()
            skills = split[1].strip()
            out += TECHNICAL_ENTRY + format_args([skill_type, skills])
        return out + '}'

    if section == 'Education':
        num = 4 # num details per entry
        out = section_name(section)
        for i in range(len(details)//num):
            entry_details = details[num*i:(i+1)*num]
            if not first_entry:
                out += SPACER
            out += EDUCATION_ENTRY + format_args(entry_details)
            first_entry = False
        return out

    if section in ('Experience', 'Projects'):
        out = section_name(section)
        while details:
            i = details.pop(0)
            if i.startswith('-'):
                if not first_entry:
                    out += SPACER
                title = ''.join(i.split('-')).strip()
                if section == 'Experience':
                    out += EXPERIENCE_ENTRY + format_args([title, details.pop(0), details.pop(0)])
                else:
                    out += PROJECT_ENTRY + format_args([title, details.pop(0)])
                first_entry = False
                continue
            out += BULLETED_DETAILS + format_args([i])
        return out

    raise Exception(f'unknown section - {section}')


def write_tex(out):
    '''write output string to .tex file'''
    with open('resume.tex', 'w', encoding='utf-8') as file:
        file.write(out)


def main():
    '''driver function'''
    lines, path = read_input()
    out = parse_input(lines)
    write_tex(out)
    os.system('latexmk -pdf -pv resume.tex')
    os.system('latexmk -c')
    pdf_path = os.path.join(path, 'resume.pdf')
    os.system(f'mv resume.pdf \'{pdf_path}\'')
    os.system('rm resume.tex')


main()
