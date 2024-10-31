import requests
import json
from datetime import datetime
import os


# Replace with your Google Apps Script URL
url = 'https://script.google.com/macros/s/AKfycbxy-Yv8_COGVOguz1cqqdt_0TxYlD6hJT_sSfzvWaLZ1nySS69-QjcNzDTAAw3b9gWW/exec'


def download_image_from_drive(drive_url, save_dir="Athlètes", filename="test.jpg"):
  # Ensure the save directory exists
  os.makedirs(save_dir, exist_ok=True)

  # Convert Google Drive link to direct download link
  if "open?id=" in drive_url:
    file_id = drive_url.split("open?id=")[-1]
  elif "file/d/" in drive_url:
    file_id = drive_url.split("file/d/")[-1].split("/view")[0]
  else:
    print("Invalid Google Drive URL format")
    return None

  download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

  try:
    # Download the image
    response = requests.get(download_url, stream=True)
    response.raise_for_status()  # Raise an error for unsuccessful responses

    # Save the image file
    file_path = os.path.join(save_dir, filename)
    with open(file_path, "wb") as file:
      file.write(response.content)

    print(f"Image downloaded successfully and saved as {file_path}")
    return file_path

  except requests.exceptions.RequestException as e:
    print(f"Failed to download image from {drive_url}: {e}")
    return None

def convert_date_format(date_str):
  if date_str == "":
    return ""
  date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
  return date_obj.strftime("%Y/%m/%d")

try:
  response = requests.get(url)
  response.raise_for_status()  # Check for request errors

  # Parse JSON data
  data = response.json()

  data_in_json = []
  # Print data or process it as needed
  print("Google Sheets Data:")
  for row in data:
    print(row)
    file_name = f"{row["Nom "].replace(" ", "_")}_{row["Prénom "].replace(" ", "_")}"
    destination = f"Athlètes/{file_name}"
    os.makedirs(destination, exist_ok=True)
    photo_url = row["Photo "]
    downloaded_image_path = download_image_from_drive(photo_url,
                                                      save_dir=destination,
                                                      filename=f"{file_name}_photo.jpg"
                                                      ) if photo_url else ""

    uploaded_cni_url = row["Télécharger la carte CNI"]
    downloaded_CNI_path = download_image_from_drive(uploaded_cni_url,
                                                    save_dir=destination,
                                                    filename=f"{file_name}_CNI.jpg"
                                                    ) if uploaded_cni_url else ""

    uploaded_passport_url = row["télécharger le Passeport"]
    downloaded_passport_path = download_image_from_drive(uploaded_passport_url,
                                                    save_dir=destination,
                                                    filename=f"{file_name}_Passeport.jpg"
                                                    ) if uploaded_passport_url else ""


    dic = {
      "photo": downloaded_image_path,
      "family_name": row["Nom "],
      "first_name": row["Prénom "],
      "date_naissance": convert_date_format(row["  Date de Naissance  "]),
      "lieu_naissance": row["Lieu de Naissance  "],
      "nationality": row["  Nationalité  "],
      "sexe": row["Sexe"],
      "blood_group": row["Groupe Sanguin  "],
      "home_address": row["Adresse du domicile  "],
      "num_téléphone": row[" N° de téléphone  "],
      "mail_address": row["Adresse mail   "],
      "facebook_address": row["Adresse facebook"],
      "full_name_pere": row["Nom et Prénom du Père  "],
      "pere_job": row["Profession du père    "],
      "full_name_mere": row["Nom et Prénom de la mère :   "],
      "mere_job": row["Profession de la mère  "],
      "num_CNI": row["N° CNI  "],
      "CNI_delivered": convert_date_format(row["CNI Délivrée le   "]),
      "CNI_expired": convert_date_format(row["CNI Expirée le "]),
      "num_passport": row["N° Passeport"],
      "passport_delivered": convert_date_format(row["Passeport Délivrée le"]),
      "discipline": row["Discipline  "],
      "taille": row["Taille  "],
      "pointure": row["Pointure  "],
      "cni_cart": downloaded_CNI_path,
      "passport": downloaded_passport_path
    }

    data_in_json.append(dic)




  with open("sheet_data.json", "w") as json_file:
    json.dump(data_in_json, json_file, indent=2)

except requests.exceptions.RequestException as e:
  print("Error fetching data:", e)

