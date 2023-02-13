\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{my_resume}[2023/02/13 A Pastel CV Template with some infographics]
\LoadClass{article}

% -------------------------------
% packages

\RequirePackage[cm]{fullpage}
\RequirePackage{geometry}
\RequirePackage{titlesec}
\RequirePackage{enumitem}
\RequirePackage[hidelinks]{hyperref}


% -------------------------------
% page formatting

\pagestyle{empty}
\geometry{margin=0.5cm}
\setlist{nosep}
\raggedright


% -------------------------------
% ATS compatibility
\input{glyphtounicode}
\pdfgentounicode=1


% -------------------------------
% text formatting

\titleformat{\section}
{\vspace{-10pt}\large\scshape}
{}{0pt}{}
[\titlerule\vspace{-5pt}]

\newcommand{\personalInfoEntry}[4]
{\begin{center}
	\textbf{\Huge #1} \\
	\small #2 $|$ 
	\href{mailto:#3}{\underline{#3}} $|$ 
	\href{https://#4}{\underline{#4}}
\end{center}}


\newcommand{\textEntry}[1]
{\begin{enumerate}[leftmargin=0.3cm, rightmargin=0.3cm, label={}]
	\item #1
\end{enumerate}}

\newcommand{\bulletedDetails}[1]
{\begin{enumerate}[left=0.6cm, rightmargin=0.3cm, label=\textbullet]
	\item #1
\end{enumerate}
}

\newcommand{\educationEntry}[4]
{\textEntry{
	\textbf{#1} \hfill #2\\
	\hspace{5pt}\textit{#3} \hfill #4
}}

\newcommand{\technicalEntry}[2]
{\textbf{#1:} #2\\}

\newcommand{\experienceEntry}[3]
{\textEntry{
	\textbf{#1} $|$ \emph{#2} \hfill #3\vspace{2pt}
}}

\newcommand{\projectEntry}[2]
{\textEntry{
	\textbf{#1} $|$ \emph{#2}
}}

\newcommand{\spacer}{\vspace{5pt}}
