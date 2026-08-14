import os

import pandas as pd
import streamlit as st
import json
import ast
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score, confusion_matrix
import numpy as np

try:
    import joblib
except Exception:
    joblib = None

try:
    from catboost import CatBoostClassifier
except Exception:
    CatBoostClassifier = None


# Categorical options as they appear (exact strings) in the training data.
TYPE_OPTIONS = ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]
CARD_TYPE_OPTIONS = ["Classic", "Gold", "Mass", "Platinum", "Signature", "Silver"]
EXP_TYPE_OPTIONS = [
    "Bills",
    "Entertainment",
    "Food",
    "Fuel",
    "Grocery",
    "Health_Fitness",
    "Home",
    "Personal_Care",
    "Travel",
]
GENDER_OPTIONS = ["F", "M"]
CITY_OPTIONS = [
    'Achalpur, India', 'Adilabad, India', 'Adityapur, India', 'Adoni, India',
    'Adoor, India', 'Afzalpur, India', 'Agartala, India', 'Agra, India',
    'Ahmedabad, India', 'Ahmednagar, India', 'Aizawl, India', 'Ajmer, India',
    'Akola, India', 'Akot, India', 'Alappuzha, India', 'Aligarh, India',
    'Alipurduar, India', 'Alirajpur, India', 'Allahabad, India', 'Alwar, India',
    'Amalapuram, India', 'Amalner, India', 'Ambejogai, India', 'Ambikapur, India',
    'Amravati, India', 'Amreli, India', 'Amritsar, India', 'Amroha, India',
    'Anakapalle, India', 'Anand, India', 'Anantapur, India', 'Anantnag, India',
    'Anjangaon, India', 'Anjar, India', 'Ankleshwar, India', 'Arakkonam, India',
    'Arambagh, India', 'Araria, India', 'Arrah, India', 'Arsikere, India',
    'Aruppukkottai, India', 'Arvi, India', 'Arwal, India', 'Asansol, India',
    'Ashok Nagar, India', 'Athni, India', 'Attingal, India', 'Aurangabad, India',
    'Azamgarh, India', 'Bagaha, India', 'Bahadurgarh, India', 'Baharampur, India',
    'Bahraich, India', 'Balaghat, India', 'Balangir, India', 'Baleshwar Town, India',
    'Ballari, India', 'Balurghat, India', 'Bankura, India', 'Bapatla, India',
    'Baramula, India', 'Barbil, India', 'Bargarh, India', 'Baripada Town, India',
    'Barnala, India', 'Barpeta, India', 'Batala, India', 'Bathinda, India',
    'Begusarai, India', 'Belagavi, India', 'Bellampalle, India', 'Bengaluru, India',
    'Bettiah, India', 'Bhabua, India', 'Bhadrachalam, India', 'Bhadrak, India',
    'Bhagalpur, India', 'Bhainsa, India', 'Bharatpur, India', 'Bharuch, India',
    'Bhatapara, India', 'Bhavnagar, India', 'Bhawanipatna, India', 'Bheemunipatnam, India',
    'Bhilai Nagar, India', 'Bhilwara, India', 'Bhimavaram, India', 'Bhiwandi, India',
    'Bhiwani, India', 'Bhongir, India', 'Bhopal, India', 'Bhubaneswar, India',
    'Bhuj, India', 'Bikaner, India', 'Bilaspur, India', 'Bobbili, India',
    'Bodhan, India', 'Bokaro Steel City, India', 'Bongaigaon City, India', 'Brahmapur, India',
    'Buxar, India', 'Byasanagar, India', 'Chaibasa, India', 'Chalakudy, India',
    'Chandausi, India', 'Chandigarh, India', 'Changanassery, India', 'Charkhi Dadri, India',
    'Chatra, India', 'Chennai, India', 'Cherthala, India', 'Chikkamagaluru, India',
    'Chilakaluripet, India', 'Chirala, India', 'Chirkunda, India', 'Chirmiri, India',
    'Chittoor, India', 'Chittur-Thathamangalam, India', 'Cuttack, India', 'Dalli-Rajhara, India',
    'Darbhanga, India', 'Darjiling, India', 'Davanagere, India', 'Deesa, India',
    'Dehradun, India', 'Dehri-on-Sone, India', 'Delhi, India', 'Deoghar, India',
    'Dhamtari, India', 'Dhanbad, India', 'Dharmanagar, India', 'Dharmavaram, India',
    'Dhenkanal, India', 'Dhoraji, India', 'Dhubri, India', 'Dhule, India',
    'Dhuri, India', 'Dibrugarh, India', 'Dimapur, India', 'Diphu, India',
    'Dumka, India', 'Dumraon, India', 'Durg, India', 'Eluru, India',
    'English Bazar, India', 'Erode, India', 'Etawah, India', 'Faridabad, India',
    'Faridkot, India', 'Farooqnagar, India', 'Fatehabad, India', 'Fatehpur Sikri, India',
    'Fazilka, India', 'Firozabad, India', 'Firozpur Cantt., India', 'Firozpur, India',
    'Forbesganj, India', 'Gadwal, India', 'Gangarampur, India', 'Ganjbasoda, India',
    'Gaya, India', 'Giridih, India', 'Goalpara, India', 'Gobichettipalayam, India',
    'Gobindgarh, India', 'Godhra, India', 'Gohana, India', 'Gokak, India',
    'Gooty, India', 'Gopalganj, India', 'Greater Mumbai, India', 'Gudivada, India',
    'Gudur, India', 'Gumia, India', 'Guntakal, India', 'Guntur, India',
    'Gurdaspur, India', 'Gurgaon, India', 'Guwahati, India', 'Gwalior, India',
    'Habra, India', 'Hajipur, India', 'Haldwani-cum-Kathgodam, India', 'Hansi, India',
    'Hapur, India', 'Hardoi , India', 'Hardwar, India', 'Hazaribag, India',
    'Hindupur, India', 'Hisar, India', 'Hoshiarpur, India', 'Hubli-Dharwad, India',
    'Hugli-Chinsurah, India', 'Hyderabad, India', 'Ichalkaranji, India', 'Imphal, India',
    'Indore, India', 'Itarsi, India', 'Jabalpur, India', 'Jagdalpur, India',
    'Jaggaiahpet, India', 'Jagraon, India', 'Jagtial, India', 'Jaipur, India',
    'Jalandhar Cantt., India', 'Jalandhar, India', 'Jalpaiguri, India', 'Jamalpur, India',
    'Jammalamadugu, India', 'Jammu, India', 'Jamnagar, India', 'Jamshedpur, India',
    'Jamui, India', 'Jangaon, India', 'Jatani, India', 'Jehanabad, India',
    'Jhansi, India', 'Jhargram, India', 'Jharsuguda, India', 'Jhumri Tilaiya, India',
    'Jind, India', 'Jodhpur, India', 'Jorhat, India', 'Kadapa, India',
    'Kadi, India', 'Kadiri, India', 'Kagaznagar, India', 'Kaithal, India',
    'Kakinada, India', 'Kalimpong, India', 'Kalpi, India', 'Kalyan-Dombivali, India',
    'Kamareddy, India', 'Kancheepuram, India', 'Kandukur, India', 'Kanhangad, India',
    'Kannur, India', 'Kanpur, India', 'Kapadvanj, India', 'Kapurthala, India',
    'Karaikal, India', 'Karimganj, India', 'Karimnagar, India', 'Karjat, India',
    'Karnal, India', 'Karur, India', 'Karwar, India', 'Kasaragod, India',
    'Kashipur, India', 'Kathua, India', 'Katihar, India', 'Kavali, India',
    'Kayamkulam, India', 'Kendrapara, India', 'Kendujhar, India', 'Keshod, India',
    'Khair, India', 'Khambhat, India', 'Khammam, India', 'Khanna, India',
    'Kharagpur, India', 'Kharar, India', 'Kishanganj, India', 'Kochi, India',
    'Kodungallur, India', 'Kohima, India', 'Kolar, India', 'Kolkata, India',
    'Kollam, India', 'Koratla, India', 'Korba, India', 'Kot Kapura, India',
    'Kothagudem, India', 'Kottayam, India', 'Kovvur, India', 'Koyilandy, India',
    'Kozhikode, India', 'Kunnamkulam, India', 'Kurnool, India', 'Kyathampalle, India',
    'Lachhmangarh, India', 'Ladnu, India', 'Ladwa, India', 'Lahar, India',
    'Laharpur, India', 'Lakheri, India', 'Lakhimpur, India', 'Lakhisarai, India',
    'Lakshmeshwar, India', 'Lal Gopalganj Nindaura, India', 'Lalitpur, India', 'Lalsot, India',
    'Lanka, India', 'Lar, India', 'Latur, India', 'Limbdi, India',
    'Lingsugur, India', 'Lonavla, India', 'Loni, India', 'Losal, India',
    'Lucknow, India', 'Ludhiana, India', 'Lumding, India', 'Lunawada, India',
    'Lunglei, India', 'Macherla, India', 'Machilipatnam, India', 'Madanapalle, India',
    'Maddur, India', 'Madhepura, India', 'Madhubani, India', 'Madhugiri, India',
    'Madhupur, India', 'Madikeri, India', 'Madurai, India', 'Mahalingapura, India',
    'Mahasamund, India', 'Mahbubnagar, India', 'Mahe, India', 'Mahemdabad, India',
    'Mahesana, India', 'Mahidpur, India', 'Mahnar Bazar, India', 'Mahuva, India',
    'Maihar, India', 'Mainaguri, India', 'Makhdumpur, India', 'Makrana, India',
    'Malaj Khand, India', 'Malappuram, India', 'Malavalli, India', 'Malegaon, India',
    'Malerkotla, India', 'Malkapur, India', 'Malout, India', 'Malpura, India',
    'Malur, India', 'Manavadar, India', 'Mancherial, India', 'Mandamarri, India',
    'Mandapeta, India', 'Mandi Dabwali, India', 'Mandi, India', 'Mandideep, India',
    'Mandla, India', 'Mandsaur, India', 'Mandvi, India', 'Mandya, India',
    'Manendragarh, India', 'Maner, India', 'Mangaluru, India', 'Manglaur, India',
    'Mangrol, India', 'Mangrulpir, India', 'Manjlegaon, India', 'Mankachar, India',
    'Manmad, India', 'Mansa, India', 'Manuguru, India', 'Manvi, India',
    'Manwath, India', 'Mapusa, India', 'Margao, India', 'Markapur, India',
    'Marmagao, India', 'Masaurhi, India', 'Mathura, India', 'Mattannur, India',
    'Mavelikkara, India', 'Mavoor, India', 'Medak, India', 'Medininagar (Daltonganj), India',
    'Medinipur, India', 'Meerut, India', 'Mehkar, India', 'Memari, India',
    'Merta City, India', 'Mhow Cantonment, India', 'Mihijam, India', 'Mira-Bhayandar, India',
    'Miryalaguda, India', 'Modasa, India', 'Modinagar, India', 'Moga, India',
    'Mohali, India', 'Mokameh, India', 'Mokokchung, India', 'Moradabad, India',
    'Morena, India', 'Morshi, India', 'Morvi, India', 'Motihari, India',
    'Mudalagi, India', 'Muddebihal, India', 'Mudhol, India', 'Muktsar, India',
    'Mulbagal, India', 'Mundi, India', 'Mungeli, India', 'Munger, India',
    'Murshidabad, India', 'Murtijapur, India', 'Murwara (Katni), India', 'Musabani, India',
    'Mussoorie, India', 'Muvattupuzha, India', 'Muzaffarpur, India', 'Mysore, India',
    'Nabadwip, India', 'Nabarangapur, India', 'Nabha, India', 'Nadbai, India',
    'Nadiad, India', 'Nagaon, India', 'Nagapattinam, India', 'Nagari, India',
    'Nagarkurnool, India', 'Nagaur, India', 'Nagda, India', 'Nagercoil, India',
    'Nagina, India', 'Nagpur, India', 'Nahan, India', 'Naharlagun, India',
    'Naidupet, India', 'Naihati, India', 'Naila Janjgir, India', 'Nainital, India',
    'Najibabad, India', 'Nakodar, India', 'Nalbari, India', 'Namakkal, India',
    'Nanded-Waghala, India', 'Nandivaram-Guduvancheri, India', 'Nandura, India', 'Nandurbar, India',
    'Nandyal, India', 'Nangal, India', 'Nanjangud, India', 'Nanjikottai, India',
    'Nanpara, India', 'Narasapuram, India', 'Narasaraopet, India', 'Narayanpet, India',
    'Nargund, India', 'Narkatiaganj, India', 'Narnaul, India', 'Narsinghgarh, India',
    'Narsipatnam, India', 'Narwana, India', 'Nashik, India', 'Nasirabad, India',
    'Nathdwara, India', 'Naugachhia, India', 'Naugawan Sadat, India', 'Nautanwa, India',
    'Navi Mumbai, India', 'Navsari, India', 'Nawabganj, India', 'Nawada, India',
    'Nawanshahr, India', 'Nawapur, India', 'Nedumangad, India', 'Neem-Ka-Thana, India',
    'Neemuch, India', 'Nehtaur, India', 'Nelamangala, India', 'Nellikuppam, India',
    'Nellore, India', 'Nepanagar, India', 'New Delhi, India', 'Neyveli (TS), India',
    'Neyyattinkara, India', 'Nidadavole, India', 'Nilambur, India', 'Nilanga, India',
    'Nimbahera, India', 'Nirmal, India', 'Nizamabad, India', 'Nohar, India',
    'Noida, India', 'Nokha, India', 'Nongstoin, India', 'Noorpur, India',
    'North Lakhimpur, India', 'Nowgong, India', 'Nuzvid, India', 'Oddanchatram, India',
    'Ongole, India', 'Orai, India', 'Osmanabad, India', 'Ottappalam, India',
    'Ozar, India', 'Pachora, India', 'Padra, India', 'Padrauna, India',
    'Paithan, India', 'Pakaur, India', 'Palacole, India', 'Palakkad, India',
    'Palani, India', 'Palanpur, India', 'Palasa Kasibugga, India', 'Palghar, India',
    'Pali, India', 'Palia Kalan, India', 'Palitana, India', 'Palladam, India',
    'Palwal, India', 'Palwancha, India', 'Panaji, India', 'Panchkula, India',
    'Pandharkaoda, India', 'Pandharpur, India', 'Pandhurna, India', 'Pandua, India',
    'Panipat, India', 'Panna, India', 'Panruti, India', 'Panvel, India',
    'Pappinisseri, India', 'Paradip, India', 'Paramakudi, India', 'Paravoor, India',
    'Parbhani, India', 'Parlakhemundi, India', 'Parli, India', 'Partur, India',
    'Parvathipuram, India', 'Pasan, India', 'Paschim Punropara, India', 'Patan, India',
    'Pathanamthitta, India', 'Pathankot, India', 'Pathri, India', 'Patiala, India',
    'Patna, India', 'Patratu, India', 'Pattamundai, India', 'Patti, India',
    'Pattukkottai, India', 'Pavagada, India', 'Pedana, India', 'Peddapuram, India',
    'Pehowa, India', 'Pen, India', 'Perambalur, India', 'Peringathur, India',
    'Perinthalmanna, India', 'Periyakulam, India', 'Periyasemur, India', 'Pernampattu, India',
    'Perumbavoor, India', 'Petlad, India', 'Phagwara, India', 'Phalodi, India',
    'Phaltan, India', 'Phulabani, India', 'Phusro, India', 'Pihani, India',
    'Pilani, India', 'Pilibanga, India', 'Pilibhit, India', 'Pilkhuwa, India',
    'Pinjore, India', 'Pipar City, India', 'Pipariya, India', 'Pithampur, India',
    'Pithapuram, India', 'Pithoragarh, India', 'Pollachi, India', 'Pondicherry, India',
    'Ponnani, India', 'Ponnur, India', 'Porbandar, India', 'Porsa, India',
    'Port Blair, India', 'Pratapgarh, India', 'Proddatur, India', 'Pudukkottai, India',
    'Pulgaon, India', 'Puliyankudi, India', 'Punalur, India', 'Punch, India',
    'Pune, India', 'Punganur, India', 'Puranpur, India', 'Puri, India',
    'Purna, India', 'Purnia, India', 'Purulia, India', 'Pusad, India',
    'Puttur, India', 'Raayachuru, India', 'Rabkavi Banhatti, India', 'Radhanpur, India',
    'Rae Bareli, India', 'Raghogarh-Vijaypur, India', 'Raghunathganj, India', 'Rahuri, India',
    'Raiganj, India', 'Raigarh, India', 'Raipur, India', 'Raisen, India',
    'Raisinghnagar, India', 'Rajagangapur, India', 'Rajahmundry, India', 'Rajakhera, India',
    'Rajampet, India', 'Rajapalayam, India', 'Rajgarh (Churu), India', 'Rajgir, India',
    'Rajkot, India', 'Rajnandgaon, India', 'Rajpipla, India', 'Rajpura, India',
    'Rajsamand, India', 'Rajula, India', 'Ramachandrapuram, India', 'Ramagundam, India',
    'Ramanagaram, India', 'Ramanathapuram, India', 'Ramdurg, India', 'Rameshwaram, India',
    'Ramganj Mandi, India', 'Ramgarh, India', 'Ramnagar, India', 'Ramngarh, India',
    'Rampur, India', 'Rampura Phul, India', 'Rampurhat, India', 'Ranaghat, India',
    'Ranavav, India', 'Ranchi, India', 'Ranebennuru, India', 'Ranibennur, India',
    'Ranipet, India', 'Rasipuram, India', 'Rasra, India', 'Ratangarh, India',
    'Rath, India', 'Ratlam, India', 'Ratnagiri, India', 'Raurkela, India',
    'Raver, India', 'Rawatbhata, India', 'Rawatsar, India', 'Raxaul Bazar, India',
    'Rayachoti, India', 'Rayadurg, India', 'Rayagada, India', 'Renukoot, India',
    'Repalle, India', 'Revelganj, India', 'Rewa, India', 'Rewari, India',
    'Rishikesh, India', 'Risod, India', 'Robertsganj, India', 'Robertson Pet, India',
    'Rohtak, India', 'Roorkee, India', 'Rosera, India', 'Rudauli, India',
    'Rudrapur, India', 'Rupnagar, India', 'Sabalgarh, India', 'Sadabad, India',
    'Sadasivpet, India', 'Sadulpur, India', 'Safidon, India', 'Sagar, India',
    'Sagara, India', 'Sagwara, India', 'Saharanpur, India', 'Saharsa, India',
    'Sahaswan, India', 'Sahibganj, India', 'Sailu, India', 'Sainthia, India',
    'Salaya, India', 'Salem, India', 'Salur, India', 'Samalkot, India',
    'Samana, India', 'Samastipur, India', 'Sambalpur, India', 'Sambhal, India',
    'Sanand, India', 'Sanawad, India', 'Sandila, India', 'Sanduru, India',
    'Sangamner, India', 'Sangareddy, India', 'Sangaria, India', 'Sangli, India',
    'Sangole, India', 'Sangrur, India', 'Sankarankoil, India', 'Sankari, India',
    'Sankeshwara, India', 'Santipur, India', 'Sarangpur, India', 'Sardarshahar, India',
    'Sardhana, India', 'Sarni, India', 'Sasaram, India', 'Sasvad, India',
    'Satana, India', 'Satara, India', 'Sathyamangalam, India', 'Satna, India',
    'Sattenapalle, India', 'Sattur, India', 'Saunda, India', 'Saundatti-Yellamma, India',
    'Savanur, India', 'Savarkundla, India', 'Savner, India', 'Sawai Madhopur, India',
    'Sedam, India', 'Sehore, India', 'Sendhwa, India', 'Seohara, India',
    'Seoni, India', 'Seoni-Malwa, India', 'Shahabad Hardoi, India', 'Shahabad Rampur, India',
    'Shahabad, India', 'Shahade, India', 'Shahbad, India', 'Shahdol, India',
    'Shahjahanpur, India', 'Shahpur, India', 'Shahpura, India', 'Shajapur, India',
    'Shamli, India', 'Shamsabad Agra, India', 'Shegaon, India', 'Sheikhpura, India',
    'Shenkottai, India', 'Sheopur, India', 'Sherghati, India', 'Sherkot, India',
    'Shikaripur, India', 'Shikarpur Bulandshahr, India', 'Shikohabad, India', 'Shillong, India',
    'Shimla, India', 'Shirdi, India', 'Shirpur-Warwade, India', 'Shirur, India',
    'Shivamogga, India', 'Shivpuri, India', 'Sholingur, India', 'Shoranur, India',
    'Shrigonda, India', 'Shrirampur, India', 'Shujalpur, India', 'Siana, India',
    'Sibsagar, India', 'Siddipet, India', 'Sidhi, India', 'Sidhpur, India',
    'Sidlaghatta, India', 'Sihor, India', 'Sihora, India', 'Sikandra Rao, India',
    'Sikandrabad, India', 'Sikar, India', 'Silchar, India', 'Siliguri, India',
    'Sillod, India', 'Simdega, India', 'Sindhagi, India', 'Sindhnur, India',
    'Singrauli, India', 'Sinnar, India', 'Sira, India', 'Sircilla, India',
    'Sirhind Fatehgarh Sahib, India', 'Sirkali, India', 'Sirohi, India', 'Sironj, India',
    'Sirsa, India', 'Sirsaganj, India', 'Sirsi, India', 'Siruguppa, India',
    'Sitamarhi, India', 'Sitapur, India', 'Sivaganga, India', 'Sivakasi, India',
    'Siwan, India', 'Sohna, India', 'Sojat, India', 'Solan, India',
    'Solapur, India', 'Sonamukhi, India', 'Sonepur, India', 'Sonipat, India',
    'Sopore, India', 'Soro, India', 'Soron, India', 'Sri Madhopur, India',
    'Srikakulam, India', 'Srikalahasti, India', 'Srinagar, India', 'Srivilliputhur, India',
    'Suar, India', 'Sugauli, India', 'Sujangarh, India', 'Sullurpeta, India',
    'Sultanganj, India', 'Sultanpur, India', 'Sumerpur, India', 'Sunabeda, India',
    'Sunam, India', 'Sundargarh, India', 'Supaul, India', 'Surandai, India',
    'Surapura, India', 'Surat, India', 'Suratgarh, India', 'Suri, India',
    'Suryapet, India', 'Tadepalligudem, India', 'Tadpatri, India', 'Taki, India',
    'Talaja, India', 'Talcher, India', 'Talegaon Dabhade, India', 'Talikota, India',
    'Taliparamba, India', 'Talode, India', 'Tamluk, India', 'Tanda, India',
    'Tandur, India', 'Tanuku, India', 'Tarakeswar, India', 'Taranagar, India',
    'Tarikere, India', 'Tarn Taran, India', 'Tasgaon, India', 'Tekkalakote, India',
    'Tenali, India', 'Tenkasi, India', 'Terdal, India', 'Tezpur, India',
    'Thakurdwara, India', 'Thana Bhawan, India', 'Thane, India', 'Thanesar, India',
    'Thangadh, India', 'Thanjavur, India', 'Tharad, India', 'Tharamangalam, India',
    'Theni Allinagaram, India', 'Thirumangalam, India', 'Thiruvalla, India', 'Thiruvallur, India',
    'Thiruvananthapuram, India', 'Thiruvarur, India', 'Thodupuzha, India', 'Thoubal, India',
    'Thrissur, India', 'Thuraiyur, India', 'Tikamgarh, India', 'Tilda Newra, India',
    'Tilhar, India', 'Tindivanam, India', 'Tinsukia, India', 'Tiptur, India',
    'Tiruchendur, India', 'Tiruchengode, India', 'Tiruchirappalli, India', 'Tirukalukundram, India',
    'Tirukkoyilur, India', 'Tirunelveli, India', 'Tirupathur, India', 'Tirupati, India',
    'Tiruppur, India', 'Tirur, India', 'Tiruttani, India', 'Tiruvannamalai, India',
    'Tiruvethipuram, India', 'Tiruvuru, India', 'Titlagarh, India', 'Tohana, India',
    'Tonk, India', 'Tuensang, India', 'Tuljapur, India', 'Tumkur, India',
    'Tumsar, India', 'Tundla, India', 'Tuni, India', 'Tura, India',
    'Uchgaon, India', 'Udaipur, India', 'Udaipurwati, India', 'Udgir, India',
    'Udhagamandalam, India', 'Udhampur, India', 'Udumalaipettai, India', 'Udupi, India',
    'Ujhani, India', 'Ujjain, India', 'Umarga, India', 'Umaria, India',
    'Umarkhed, India', 'Umbergaon, India', 'Umred, India', 'Umreth, India',
    'Una, India', 'Unjha, India', 'Unnao, India', 'Upleta, India',
    'Uran Islampur, India', 'Uran, India', 'Uravakonda, India', 'Usilampatti, India',
    'Uthamapalayam, India', 'Utraula, India', 'Vadakkuvalliyur, India', 'Vadalur, India',
    'Vadipatti, India', 'Vadnagar, India', 'Vadodara, India', 'Vaijapur, India',
    'Valparai, India', 'Valsad, India', 'Vandavasi, India', 'Vaniyambadi, India',
    'Vapi, India', 'Varanasi, India', 'Varkala, India', 'Vasai-Virar, India',
    'Vatakara, India', 'Vedaranyam, India', 'Vellakoil, India', 'Vellore, India',
    'Venkatagiri, India', 'Veraval, India', 'Vidisha, India', 'Vijainagar Ajmer, India',
    'Vijayapura, India', 'Vijayawada, India', 'Vikarabad, India', 'Vikramasingapuram, India',
    'Viluppuram, India', 'Vinukonda, India', 'Viramgam, India', 'Virudhachalam, India',
    'Virudhunagar, India', 'Visakhapatnam, India', 'Visnagar, India', 'Vita, India',
    'Vizianagaram, India', 'Vrindavan, India', 'Vyara, India', 'Wadgaon Road, India',
    'Wadhwan, India', 'Wadi, India', 'Wai, India', 'Wanaparthy, India',
    'Wani, India', 'Wankaner, India', 'Warangal, India', 'Wardha, India',
    'Warisaliganj, India', 'Warora, India', 'Washim, India', 'Wokha, India',
    'Yadgir, India', 'Yamunanagar, India', 'Yanam, India', 'Yavatmal, India',
    'Yawal, India', 'Yellandu, India', 'Yemmiganur, India', 'Yerraguntla, India',
    'Yevla, India', 'Zaidpur, India', 'Zamania, India', 'Zira, India',
    'Zirakpur, India', 'Zunheboto, India',
]


# Feature order must match the trained model (notebook X = df.drop(['Date','isFraud','Month_name'])).
# The model is trained on integer Day/Month/Year, NOT on the raw Date column.
EXPECTED_FEATURES = [
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "City",
    "type",
    "Card Type",
    "Exp Type",
    "Gender",
    "Day",
    "Month",
    "Year",
]


def load_model_from_file(path):
    if path is None:
        return None
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    if ext in (".pkl", ".joblib"):
        if joblib is None:
            raise RuntimeError("joblib is not available in this environment")
        return joblib.load(path)
    if ext in (".cbm", ".bin"):
        if CatBoostClassifier is None:
            raise RuntimeError("catboost is not installed in this environment")
        model = CatBoostClassifier()
        model.load_model(path)
        return model
    # try pickle fallback
    try:
        import pickle

        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception:
        raise RuntimeError(f"Unsupported model format: {ext}")


def predict(model, X: pd.DataFrame):
    # Try sklearn-like predict_proba
    try:
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)
            # assume binary, take class 1 probability
            prob = float(proba[0][1])
            pred = int((prob >= 0.5))
            return pred, prob
    except Exception:
        pass

    # CatBoostClassifier object path: try model.predict_proba
    try:
        if hasattr(model, "predict") and hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)
            prob = float(proba[0][1])
            pred = int((prob >= 0.5))
            return pred, prob
    except Exception:
        pass

    # fallback to predict
    try:
        pred = model.predict(X)
        pred = int(pred[0])
        return pred, None
    except Exception as e:
        raise RuntimeError(f"Model prediction failed: {e}")


def build_input_dataframe(values: dict) -> pd.DataFrame:
    # Build DataFrame in the exact feature order the model was trained on.
    row = {k: values.get(k, None) for k in EXPECTED_FEATURES}
    # numeric conversions
    for num in ("amount", "oldbalanceOrg", "newbalanceOrig"):
        v = row.get(num)
        try:
            row[num] = float(v) if v not in (None, "") else 0.0
        except Exception:
            row[num] = 0.0
    # Day / Month / Year are integer features entered directly by the user.
    for intcol in ("Day", "Month", "Year"):
        v = row.get(intcol)
        try:
            row[intcol] = int(v) if v not in (None, "") else 0
        except Exception:
            row[intcol] = 0
    return pd.DataFrame([row])


def train_model_from_csv(uploaded_file, params):
    if uploaded_file is None:
        raise RuntimeError("No dataset provided")
    if CatBoostClassifier is None:
        raise RuntimeError("CatBoost is not installed in this environment")

    df = pd.read_csv(uploaded_file)
    # Drop nameOrig if present
    if "nameOrig" in df.columns:
        df = df.drop(["nameOrig"], axis=1)

    # Parse Date if present
    if "Date" in df.columns:
        try:
            df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")
        except Exception:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Day"] = df["Date"].dt.day
        df["Month"] = df["Date"].dt.month
        df["Year"] = df["Date"].dt.year
        df["Month_name"] = df["Date"].dt.month_name()

    # Prepare X,y
    if "isFraud" not in df.columns:
        raise RuntimeError("Dataset must contain 'isFraud' target column")

    X = df.copy()
    drop_cols = [c for c in ["Date", "Month_name"] if c in X.columns]
    X = X.drop(drop_cols + ["isFraud"], axis=1, errors="ignore")
    y = df["isFraud"]

    categorical_features = [c for c in ["City", "type", "Card Type", "Exp Type", "Gender"] if c in X.columns]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model_params = params.copy()
    if "class_weights" not in model_params:
        model_params["class_weights"] = [1, 4.5]

    model = CatBoostClassifier(**model_params)

    model.fit(X_train, y_train, cat_features=categorical_features if len(categorical_features) else None,
              eval_set=(X_test, y_test), early_stopping_rounds=20)

    y_pred = model.predict(X_test)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    models_dir = os.path.join(os.getcwd(), "streamlit_app", "models")
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, "catboost_model.cbm")
    model.save_model(model_path)

    return model, model_path, {"recall": recall, "precision": precision, "confusion_matrix": cm}


def main():
    st.set_page_config(page_title="Bank Transaction Fraud Predictor", layout="centered")
    st.title("Bank Transaction Fraud Detection — Predict")

    st.markdown(
        "Upload a trained model file (`.pkl`, `.joblib`, or CatBoost `.cbm`).\n\nIf you don't have a file yet, place it in `streamlit_app/models/` and reload."
    )

    # Sidebar: model options
    with st.sidebar.expander("Model"):
        uploaded = st.file_uploader("Upload model file (.pkl/.joblib/.cbm)", type=["pkl", "joblib", "cbm", "bin"])
        model_path_input = st.text_input("Or local model path (relative to repo)", value="Fraud_catboost_classifier.joblib")
        st.markdown("---")
        use_catboost_default = st.checkbox("Prefer CatBoost and use notebook defaults if no model provided", value=True)
        st.markdown("**CatBoost defaults (from notebook):**")
        st.caption("iterations=700, learning_rate=0.05, depth=4, class_weights=[1,4.5], l2_leaf_reg=3")
        st.caption("random_strength=1, bagging_temperature=1, eval_metric='AUC'")

    model = None
    # prefer uploaded
    if uploaded is not None:
        temp_path = os.path.join(".", "streamlit_uploaded_model")
        with open(temp_path, "wb") as f:
            f.write(uploaded.getbuffer())
        try:
            model = load_model_from_file(temp_path)
        except Exception as e:
            st.sidebar.error(f"Failed to load uploaded model: {e}")
    else:
        if os.path.exists(model_path_input):
            try:
                model = load_model_from_file(model_path_input)
            except Exception as e:
                st.sidebar.error(f"Failed to load model at {model_path_input}: {e}")

    # If still no model and the user wants CatBoost defaults, instantiate default CatBoostClassifier
    if model is None and use_catboost_default:
        if CatBoostClassifier is None:
            st.sidebar.warning("CatBoost is not installed; add 'catboost' to requirements.txt to enable defaults.")
        else:
            default_params = dict(
                iterations=700,
                learning_rate=0.05,
                depth=4,
                loss_function='Logloss',
                eval_metric='AUC',
                class_weights=[1, 4.5],
                l2_leaf_reg=3,
                random_strength=1,
                bagging_temperature=1,
                verbose=0,
            )
            try:
                model = CatBoostClassifier(**default_params)
                st.sidebar.info("Default CatBoostClassifier instantiated (untrained). Upload a trained .cbm to make predictions.")
            except Exception as e:
                st.sidebar.error(f"Failed to instantiate CatBoostClassifier: {e}")

    if model is None:
        st.warning("No model loaded yet. Upload a model or place it at the local path and reload.")

    # Training UI: allow user to upload dataset and run training locally
    with st.sidebar.expander("Train model from dataset"):
        data_upload = st.file_uploader("Upload dataset CSV to train model", type=["csv"], key="train_csv")
        train_button = st.button("Train CatBoost model using notebook pipeline")

    if train_button:
        try:
            # Try to parse notebook params
            nb_path = os.path.join(os.getcwd(), "notebooks", "Bank_transaction_fraud_detection.ipynb")
            nb_params = None
            try:
                with open(nb_path, "r", encoding="utf-8") as f:
                    nb = json.load(f)
                for cell in nb.get("cells", []):
                    if cell.get("cell_type") != "code":
                        continue
                    src = "".join(cell.get("source", []))
                    if "final_model = CatBoostClassifier" in src:
                        idx = src.find("CatBoostClassifier")
                        idx = src.find("(", idx)
                        count = 0
                        end = None
                        for i in range(idx, len(src)):
                            if src[i] == "(":
                                count += 1
                            elif src[i] == ")":
                                count -= 1
                                if count == 0:
                                    end = i
                                    break
                        if end:
                            params_str = src[idx + 1: end]
                            ps = re.sub(r"\s+", " ", params_str.strip())
                            ps2 = re.sub(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=", r'"\1":', ps)
                            dict_str = "{" + ps2 + "}"
                            try:
                                nb_params = ast.literal_eval(dict_str)
                            except Exception:
                                nb_params = None
                        break
            except Exception:
                nb_params = None

            if nb_params is None:
                nb_params = dict(iterations=700, learning_rate=0.05, depth=4, loss_function="Logloss",
                                 eval_metric="AUC", class_weights=[1, 4.5], l2_leaf_reg=3,
                                 random_strength=1, bagging_temperature=1, verbose=100)

            with st.spinner("Training model — this may take several minutes..."):
                model_trained, model_path, metrics = train_model_from_csv(data_upload, nb_params)
            st.success(f"Training finished. Model saved to {model_path}")
            st.write("Metrics:", metrics)
            model = model_trained
        except Exception as e:
            st.error(f"Training failed: {e}")

    st.subheader("Transaction input")
    with st.form("input_form"):
        col_d, col_m, col_y = st.columns(3)
        with col_d:
            day = st.number_input("Day", min_value=1, max_value=31, value=1, step=1, format="%d")
        with col_m:
            month = st.number_input("Month", min_value=1, max_value=12, value=1, step=1, format="%d")
        with col_y:
            year = st.number_input("Year", min_value=2000, max_value=2100, value=2025, step=1, format="%d")
        amount = st.number_input("Amount", min_value=0.0, value=0.0, format="%.2f")
        oldbalanceOrg = st.number_input("Old Balance Origin", min_value=0.0, value=0.0, format="%.2f")
        newbalanceOrig = st.number_input("New Balance Origin", min_value=0.0, value=0.0, format="%.2f")
        City = st.selectbox("City", CITY_OPTIONS)
        ttype = st.selectbox("Type", TYPE_OPTIONS)
        card_type = st.selectbox("Card Type", CARD_TYPE_OPTIONS)
        exp_type = st.selectbox("Exp Type", EXP_TYPE_OPTIONS)
        gender = st.selectbox("Gender", GENDER_OPTIONS)

        submitted = st.form_submit_button("Predict")

    if submitted:
        if model is None:
            st.error("Please upload or provide a valid model before predicting.")
            return

        vals = {
            "amount": amount,
            "oldbalanceOrg": oldbalanceOrg,
            "newbalanceOrig": newbalanceOrig,
            "City": City,
            "type": ttype,
            "Card Type": card_type,
            "Exp Type": exp_type,
            "Gender": gender,
            "Day": day,
            "Month": month,
            "Year": year,
        }

        X = build_input_dataframe(vals)

        try:
            pred, prob = predict(model, X)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            return

        st.write("**Prediction**")
        if prob is None:
            st.info(f"Predicted class: {pred}")
        else:
            st.info(f"Predicted class: {pred} — probability fraud: {prob:.3f}")


if __name__ == "__main__":
    main()
