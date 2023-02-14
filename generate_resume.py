import sys
import os

# following characters are not supported - ~, ^, \

slash = '\\'

def read_input(args):
    if len(sys.argv) < 2:
        print('usage: python3 generate_resume.py text_file')
        return

    infile = sys.argv[1]
    if not os.path.isfile(infile):
        print('file does not exist')
        return

    with open(infile, 'r', encoding='utf8') as f:
        lines = f.readlines()

    return lines


special = ['&', '%', '$', '#', '_', '{', '}']
def replaceSpecial(st):
    for i in special:
        st = st.replace(i, slash + i)
    return st


def parse_input(lines):
    out = slash + 'documentclass{resume}'
    out += slash + 'begin{document}'
    while lines:
        curr = lines.pop(0).strip()
        if not curr.startswith('--'): # skip until next section start
            continue

        section = ''.join(curr.split('--')).strip()
        details = []

        curr = replaceSpecial(lines.pop(0).strip())
        while curr != '====': # until end of section
            if curr: # omit blank lines
                details.append(curr)
            curr = replaceSpecial(lines.pop(0).strip())

        out += formatInfo(section, details)

    return out + slash + 'end{document}'


def checkNumFields(section, lst, n, mode='s'):
    if not len(lst) == n:
        raise Exception(f'{section}' + 'section' if mode =='s' else 'entries' + 'must have {n} detail(s)')


def formatArgs(details):
    st = ''
    for i in details:
        st += '{' + i + '}'
    return st


def sectionName(section):
    return slash + f'section{{{section}}}'


personalInfoEntry = slash + 'personalInfoEntry'
textEntry = slash + 'textEntry'
technicalEntry = slash + 'technicalEntry'
educationEntry = slash + 'educationEntry'
experienceEntry = slash + 'experienceEntry'
projectEntry = slash + 'projectEntry'
bulletedDetails = slash + 'bulletedDetails'
spacer = slash + 'spacer'


def formatInfo(section, details):
    first_entry = True

    if section == 'Personal':
        checkNumFields(section, details, 4)
        return personalInfoEntry + formatArgs(details)

    if section in ('Objective', 'Coursework'):
        checkNumFields(section, details, 1)
        return sectionName(section) + textEntry + formatArgs(details)

    if section == 'Technical Skills':
        out = sectionName(section) + textEntry + '{'
        for i in details:
            split = i.split('-')
            type = split[0].strip()
            skills = split[1].strip()
            out += technicalEntry + formatArgs([type,skills])
        return out + '}'

    if section == 'Education':
        l = 4 # num details per entry
        out = sectionName(section)
        for i in range(len(details)//l):
            entry_details = details[l*i:(i+1)*l]
            if not first_entry:
                out += spacer
            out += educationEntry + formatArgs(entry_details)
            first_entry = False
        return out

    if section in ('Experience', 'Projects'):
        out = sectionName(section)
        while details:
            i = details.pop(0)
            if i.startswith('-'):
                if not first_entry:
                    out += spacer
                title = ''.join(i.split('-')).strip()
                if section == 'Experience':
                    out += experienceEntry + formatArgs([title, details.pop(0), details.pop(0)])
                else:
                    out += projectEntry + formatArgs([title, details.pop(0)])
                first_entry = False
                continue
            out += bulletedDetails + formatArgs([i])
        return out

    raise Exception(f'unknown section - {section}')


def write_tex(st):
    with open('resume.tex', 'w') as f:
        f.write(st)


def main():
    lines = read_input(sys.argv)
    out = parse_input(lines)
    write_tex(out)
    os.system('latexmk -pdf -pv resume.tex')
    os.system('latexmk -c')
    os.system('rm resume.tex')

main()
