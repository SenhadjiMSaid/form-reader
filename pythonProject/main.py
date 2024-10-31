import json
from pandas.io.formats.format import return_docstring
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import os

from pythonProject.read_form import file_name


def read_data_from_json(file_path):
  with open(file_path, "r", encoding="utf-8") as file:
    return json.load(file)


def generate_athlete_info_pdf(data, filename="filled_athlete_info.pdf"):
  # Initialize canvas
  c = canvas.Canvas(filename, pagesize=A4)
  width, height = A4

  rect_x = width / 4
  rect_y = height - 100
  rect_width = 275
  rect_height = 50
  shadow_offset = 3

  # Set up font and title
  # c.setFont("Helvetica-Bold", 16)
  # c.drawString(300, height - 75, "Fiche de Renseignement Athlète")
  # c.drawString(375, height - 90, "2024-2025")
  c.setFillColor(colors.grey)
  c.rect(rect_x + shadow_offset, rect_y - shadow_offset, rect_width, rect_height, fill=True, stroke=0)
  c.setFillColor(colors.lightgrey)  # Light gray for main rectangle
  c.rect(rect_x, rect_y, rect_width, rect_height, fill=True, stroke=0)
  c.setFillColor(colors.black)
  c.setFont("Helvetica-Bold", 14)
  c.drawCentredString(rect_x + rect_width / 2 + 15, rect_y + rect_height / 4 + 15, "Fiche de Renseignement Athlète")
  c.drawCentredString(rect_x + rect_width / 2 - 5, rect_y + rect_height / 4 - 5, "2024 - 2025")

  logo_path = "logo.jpg"
  logo = ImageReader(logo_path)
  c.drawImage(logo, x= 40, y=height - 120, width=100, height=100)

  # Add Photo Placeholder
  photo_path = data.get("photo")
  if photo_path and os.path.isfile(photo_path):
    c.drawImage(photo_path, 450, height - 120, width=80, height=100)
  else:
    c.rect(450, height - 120, 80, 100)  # Placeholder box for photo
    c.drawString(475, height - 110, "PHOTO")

  # Basic information
  y_position = height - 200
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, "Nom :")
  c.setFont("Helvetica", 12)
  c.drawString(150, y_position, f"{data.get('family_name', '')}")
  c.setFont("Helvetica-Bold", 12)
  c.drawString(300, y_position, "Prénom: ")
  c.setFont("Helvetica", 12)
  c.drawString(360, y_position, f"{data.get('first_name', '')}")

  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"Date et Lieu de Naissance: ")
  c.setFont("Helvetica", 12)
  c.drawString(260, y_position, f"{data.get('date_naissance', '')} à {data.get('lieu_naissance', '')}")

  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"Nationalité: ")
  c.setFont("Helvetica", 12)
  c.drawString(170, y_position, f"{data.get('nationality', '')}")
  c.setFont("Helvetica-Bold", 12)
  c.drawString(250, y_position, f"Sexe: ")
  c.setFont("Helvetica", 12)
  c.drawString(285, y_position, f"{data.get('sexe', '')}")
  c.setFont("Helvetica-Bold", 12)
  c.drawString(350, y_position, f"Groupe Sanguin: ")
  c.setFont("Helvetica", 12)
  c.drawString(450, y_position, f"{data.get('blood_group', '')}")

  y_position -= 20
  c.setStrokeColor(colors.black)
  c.setLineWidth(1)  # Set the line thickness
  c.line(100, y_position, width - 50, y_position)

  # Contact details
  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"Adresse du domicile: ")
  c.setFont("Helvetica", 12)
  c.drawString(225, y_position, f"{data.get('home_address', '')}")

  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"N° de téléphone: ")
  c.setFont("Helvetica", 12)
  c.drawString(200, y_position, f"{data.get('num_téléphone', '')}")

  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"Adresse mail: ")
  c.setFont("Helvetica", 12)
  c.drawString(185, y_position, f"{data.get('mail_address', '')}")
  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"Adresse Facebook: ")
  c.setFont("Helvetica", 12)
  c.drawString(220, y_position, f"{data.get('facebook_address', '')}")

  y_position -= 20
  c.setStrokeColor(colors.black)
  c.setLineWidth(1)  # Set the line thickness
  c.line(100, y_position, width - 50, y_position)

  # ID details
  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"N° CNI: ")
  c.setFont("Helvetica", 12)
  c.drawString(216, y_position, f"{data.get('num_CNI', '')}")
  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"Délivrée le: ")
  c.setFont("Helvetica", 12)
  c.drawString(220, y_position, f"{data.get('CNI_delivered', '')}")
  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"Expirée le: ")
  c.setFont("Helvetica", 12)
  c.drawString(220, y_position, f"{data.get('CNI_expired', '')}")

  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"N° Passeport: ")
  c.setFont("Helvetica", 12)
  c.drawString(216, y_position, f"{data.get('num_passport', '')}")
  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"Délivrée le: ")
  c.setFont("Helvetica", 12)
  c.drawString(220, y_position, f"{data.get('passport_delivered', '')}")

  y_position -= 20
  c.setStrokeColor(colors.black)
  c.setLineWidth(1)  # Set the line thickness
  c.line(100, y_position, width - 50, y_position)

  # Physical attributes
  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"Discipline: ")
  c.setFont("Helvetica", 12)
  c.drawString(175, y_position, f"{data.get('discipline', '')}")
  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"Taille: ")
  c.setFont("Helvetica", 12)
  c.drawString(175, y_position, f"{data.get('taille', '')}")
  y_position -= 20
  c.setFont("Helvetica-Bold", 12)
  c.drawString(100, y_position, f"Pointure: ")
  c.setFont("Helvetica", 12)
  c.drawString(175, y_position, f"{data.get('pointure', '')}")

  y_position -= 20
  c.setStrokeColor(colors.black)
  c.setLineWidth(2)  # Set the line thickness
  c.line(223, 100, 375, 100)

  c.setFont("Helvetica-Bold", 10)
  c.drawCentredString(x=width / 2, y=80, text="Siège : Palais des Sports ORAN")
  c.drawCentredString(x=width / 2, y=65, text="Mail : nrcovb@hotmail.fr")
  c.drawCentredString(x=width / 2, y=50, text="Mob : 07.73.92.64.61")


  # Save the PDF
  c.save()



data = read_data_from_json('sheet_data.json')
for athlete in data:
  print(f"{athlete['family_name'].replace(' ', '_')}_{athlete['first_name'].replace(' ', '_')}")
  file_name = f"{athlete['family_name'].replace(' ', '_')}_{athlete['first_name'].replace(' ', '_')}"
  print(athlete)
  generate_athlete_info_pdf(athlete, filename=f"Athlètes/{file_name}/{file_name}.pdf")


