import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.models import Template, TemplateCategory

class TemplateManager:
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir
        self._ensure_templates_dir()
        
        # Load default templates
        self.default_templates = {
            'ieee': self._get_ieee_template(),
            'mdpi': self._get_mdpi_template(),
            'springer': self._get_springer_template()
        }
    
    def _ensure_templates_dir(self):
        """Ensure templates directory exists."""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
    
    def _get_ieee_template(self) -> Dict[str, Any]:
        """Get IEEE template structure."""
        return {
            'name': 'IEEE',
            'description': 'IEEE Conference Paper Template',
            'format': 'ieee',
            'content': r'''\documentclass[conference]{IEEEtran}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{cite}
\usepackage{url}

\title{\LARGE\bf Title of the Paper}

\author{\IEEEauthorblockN{Author Name}}
\IEEEauthorblockA{Institution\\Email: author@example.com}}

\begin{document}
\maketitle
\begin{abstract}
Abstract goes here.
\end{abstract}

\section{Introduction}
Introduction goes here.

\section{Related Work}
Related work goes here.

\section{Methodology}
Methodology goes here.

\section{Experiments}
Experiments go here.

\section{Results}
Results go here.

\section{Conclusion}
Conclusion goes here.

\section*{Acknowledgment}
Acknowledgment goes here.

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}''',
            '                'format':metadata': {
 'ieee',
                'version': '1.0',
                'last_updated': datetime.utcnow().isoformat()
            }
        }
    
    def _get_mdpi_template(self) -> Dict[str, Any]:
        """Get MDPI template structure."""
        return {
            'name': 'MDPI',
            'description': 'MDPI Journal Article Template',
            'format': 'mdpi',
            'content': r'''\documentclass[journal,article,submit,pdftex]{Definitions/mdpi}

\title{Title of the Paper}

\author{Author Name}
\affiliation{Institution}
\email{author@example.com}

\begin{abstract}
Abstract goes here.
\end{abstract}

\introduction
Introduction goes here.

\section{Section 1}
Section 1 content goes here.

\section{Section 2}
Section 2 content goes here.

\section{Results and Discussion}
Results and discussion go here.

\section{Conclusions}
Conclusions go here.

\end{document}''',
            'metadata': {
                'format': 'mdpi',
                'version': '1.0',
                'last_updated': datetime.utcnow().isoformat()
            }
        }
    
    def _get_springer_template(self) -> Dict[str, Any]:
        """Get Springer template structure."""
        return {
            'name': 'Springer',
            'description': 'Springer Lecture Notes in Computer Science Template',
            'format': 'springer',
            'content': r'''\documentclass{llncs}
\usepackage{amsmath}
\usepackage{graphicx}

\title{Title of the Paper}

\author{Author Name}

\institute{Institution}

\begin{document}
\maketitle

\begin{abstract}
Abstract goes here.
\end{abstract}

\section{Introduction}
Introduction goes here.

\section{Related Work}
Related work goes here.

\section{Methodology}
Methodology goes here.

\section{Experiments}
Experiments go here.

\section{Results}
Results go here.

\section{Conclusion}
Conclusion goes here.

\end{document}''',
            'metadata': {
                'format': 'springer',
                'version': '1.0',
                'last_updated': datetime.utcnow().isoformat()
            }
        }
    
    def get_template(self, template_format: str, db: Session) -> Dict[str, Any]:
        """Get a template by format."""
        # Check if it's a default template
        if template_format in self.default_templates:
            return self.default_templates[template_format]
        
        # Check database for user templates
        db_template = db.query(Template).filter(
            Template.type == 'global',
            Template.format == template_format
        ).first()
        
        if db_template:
            return {
                'name': db_template.name,
                'description': 'Custom template',
                'format': template_format,
                'content': db_template.content,
                'metadata': {
                    'format': template_format,
                    'version': '1.0',
                    'last_updated': db_template.updated_at.isoformat() if db_template.updated_at else datetime.utcnow().isoformat()
                }
            }
        
        return None
    
    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Get all available templates."""
        templates = []
        
        # Add default templates
        for key, template in self.default_templates.items():
            templates.append({
                'key': key,
                'name': template['name'],
                'description': template['description'],
                'format': template['format']
            })
        
        return templates
    
    def create_custom_template(self, name: str, content: str, format: str, db: Session, user_id: int) -> Template:
        """Create a custom template."""
        db_template = Template(
            name=name,
            type='user',
            content=content,
            visibility='private',
            owner_id=user_id,
            created_at=datetime.utcnow()
        )
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        
        return db_template
    
    def apply_template(self, template_format: str, content: str, metadata: Dict[str, Any], db: Session) -> str:
        """Apply a template to content."""
        template = self.get_template(template_format, db)
        
        if not template:
            # Return plain content if template not found
            return content
        
        # Replace placeholders in template with actual content
        latex_content = template['content']
        
        # Replace title
        if 'title' in metadata:
            latex_content = latex_content.replace('Title of the Paper', metadata['title'])
        
        # Replace author
        if 'author' in metadata:
            latex_content = latex_content.replace('Author Name', metadata['author'])
        
        # Replace abstract
        if 'abstract' in metadata:
            # Simple replacement - in real implementation, this would be more sophisticated
            latex_content = latex_content.replace('Abstract goes here.', metadata['abstract'])
        
        # Replace sections
        sections = ['introduction', 'related_work', 'methodology', 'experiments', 'results', 'conclusion']
        for i, section in enumerate(sections):
            section_key = f'section_{i+1}'
            if section_key in metadata:
                section_name = section.replace('_', ' ').title()
                latex_content = latex_content.replace(
                    f'Section {i+1} content goes here.',
                    f'\section{{{section_name}}}\n{metadata[section_key]}'
                )
        
        return latex_content
    
    def validate_template(self, template_content: str) -> Dict[str, Any]:
        """Validate a LaTeX template."""
        # Basic validation checks
        checks = {
            'has_documentclass': r'\documentclass' in template_content,
            'has_begin_document': r'\begin{document}' in template_content,
            'has_end_document': r'\end{document}' in template_content,
            'has_title': r'\title' in template_content or r'\maketile' in template_content,
            'has_author': r'\author' in template_content,
            'has_maketile': r'\maketile' in template_content or r'\title' in template_content
        }
        
        is_valid = all(checks.values())
        
        return {
            'is_valid': is_valid,
            'checks': checks,
            'message': 'Template is valid' if is_valid else 'Template has missing elements'
        }
    
    def export_template(self, template_format: str, db: Session) -> Dict[str, Any]:
        """Export a template."""
        template = self.get_template(template_format, db)
        
        if not template:
            return {
                'success': False,
                'message': f'Template {template_format} not found',
                'data': None
            }
        
        # Save to file
        template_file = os.path.join(self.templates_dir, f'{template_format}.tex')
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template['content'])
        
        return {
            'success': True,
            'message': f'Template {template_format} exported successfully',
            'data': {
                'file_path': template_file,
                'template': template
            }
        }

# Create a global template manager instance
template_manager = TemplateManager()