# STUDIESTARTSSPILGENERATOREN
# Script by: Annekatrine Kirketerp-Møller

####################################################################
############################# SETTINGS #############################
####################################################################

# Navnet du gerne vil have selve spil-filen får når den eksporterer:

spil_navn = 'eksempel-spil'

# # Navnet på den fil, hvor spillets data ligger:
csv_navn = 'spil.csv'

# # Navn på mappen med billederne i:
mappe_navn = 'billede_mappe'

# # Default farve, som felterne bliver bliver hvis ikke farve skrives i sheetet:
default_farve = 'white'

# # Navn på billedet, som skal være i midten (reglerne)
# # Dimensioner anbefales at være omkring 1:1.06 (dvs. næsten kvadratisk)
# # Billedet bliver resizet til at være 4584x4323px for at passe i midten
center_img_sti = 'regler.jpg'

####################################################################
############################## SCRIPT ##############################
####################################################################

from PIL import Image, ImageDraw, ImageFont

# Hent csv-data
spil_data = {'titel':[],'tekst':[],'billeder':[],'billede_retning':[],'farver':[]}
with open(csv_navn) as data_file:
    for line in data_file:
        if '.tsv' in csv_navn:
            data_unstrip = line.split('\t')
            data = []
            for elm in data_unstrip:
                data.append(elm.strip())
        else:
            data = line.strip().split(';')
        if line.startswith('#'):
            pass
        elif data[0].strip() == 'Start-felt':
            start_farve = data[1].strip()
            start_tekst_farve = data[2].strip()
        else:
            spil_data['titel'].append(str(data[0].strip().upper()))
            spil_data['tekst'].append(str(data[4]))
            spil_data['billeder'].append(f'{mappe_navn}/{data[1].strip()}')
            spil_data['billede_retning'].append(str(data[2].strip().upper()))
            if str(data[3].strip().lower()) == '':
                spil_data['farver'].append(default_farve)
            else:
                spil_data['farver'].append(str(data[3].strip().lower()))

# Sørg for at der er det korrekte antal felter:

antal_spilfelter = 68 # eksl. start

# Autofyld med hvide felter, hvis ikke csv filen har nok felter:
if not len(spil_data['titel']) == len(spil_data['tekst']) == len(spil_data['billeder']) == len(spil_data['billede_retning']) == len(spil_data['farver']):
    print('Alle felter var ikke korrekt udfyldt, husk at der som minimum skal være tekst til hvert felt')
    exit()
elif len(spil_data['tekst']) == antal_spilfelter:
    print('Du har udfyldt alle felter!')
else:
    print('Ikke alle felter er udfyldt, der genereres automatisk place-holder felter.')
    i = 0
    tomme_felter = antal_spilfelter - len(spil_data['titel'])
    while i < tomme_felter:
        spil_data['titel'].append('')
        spil_data['tekst'].append(f'placeholder{i+len(spil_data['titel'])}')
        spil_data['billeder'].append('')
        spil_data['billede_retning'].append('')
        spil_data['farver'].append('white')
        i +=1

# Generer selve billedet:

img_size = (14043,9933)

spillet = Image.new('RGB',img_size,color='white')
spillet_gen = ImageDraw.Draw(spillet)

def font_size_def(size):
    return ImageFont.truetype('font.ttf',size)

pos = (0,0)

spillet_gen.rectangle(((pos[0]+50,pos[1]+50),(img_size[0]-50,img_size[1]-50)),fill='black')

pos = (50,9933-50)
thick_line_dim = 20
thin_line_dim = 10

felt_dims_width = int((img_size[0]-100-(2*thick_line_dim)-(thin_line_dim*9))/9)
felt_dims_height = int((img_size[1]-100-(2*thick_line_dim)-(thin_line_dim*8))/9)

felt_dims = (felt_dims_width,felt_dims_height)

###  Start feltet

felt = Image.new('RGB',felt_dims,color=start_farve)

felt_draw = ImageDraw.Draw(felt)

font = font_size_def(250)

start_t_dims = font.getbbox('START')

felt_draw.text(((felt_dims[0]/2)-(start_t_dims[2]/2),(felt_dims[1]/2)-(start_t_dims[3]/2)),'START',fill=start_tekst_farve,font=font)

# Initialiser listen, som skal indeholde alle felterne
felter = [felt]

# Funktion, der får billederne til at passe ind i feltet
def resize_image(image: Image.Image, max_width: int = None, max_height: int = None) -> Image.Image:
    if not max_width and not max_height:
        raise ValueError("Either max_width or max_height must be specified.")
    
    # Get the original dimensions of the image
    original_width, original_height = image.size

    # Calculate the aspect ratio of the image
    aspect_ratio = original_width / original_height

    # Determine the new dimensions while maintaining the aspect ratio
    if max_width and max_height:
        raise ValueError("Specify only one of max_width or max_height.")
    elif max_width:
        new_width = max_width
        new_height = int(new_width / aspect_ratio)
        if new_height > felt_dims_height-40:
            new_height = felt_dims_height-40
            new_width = int(new_height * aspect_ratio)
    elif max_height:
        new_height = max_height
        new_width = int(new_height * aspect_ratio)
        if new_width > felt_dims_width-40:
            new_width = felt_dims_width-40
            new_height = int(new_width / aspect_ratio)

    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    return resized_image

# Funktion, der får teksten til at passe ind i den givne plads med størst mulige skrifttype og genererer et billede med teksten på, som kan sættes ind i feltet
def create_text_element(text: str, max_width: int, max_height: int, bg_color: str, title: str = None) -> Image.Image:
    if not max_width or not max_height:
        raise ValueError("Both max_width and max_height must be specified.")

    # Function to wrap text to fit within the given width
    def text_wrap(draw, text, font, max_width):
        words = text.split(' ')
        lines = []
        line = ''
        for word in words:
            test_line = line + word + ' '
            width, _ = draw.textbbox((0, 0), test_line, font=font)[2:]
            if width <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word + ' '
        lines.append(line)
        return lines

    # Function to get the size of multiline text
    def draw_multiline_text_size(draw, lines, font):
        max_width = 0
        total_height = 0
        for line in lines:
            width, height = draw.textbbox((0, 0), line, font=font)[2:]
            max_width = max(max_width, width)
            total_height += height
        return max_width, total_height

    # Create a dummy image to draw the text
    dummy_image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(dummy_image)
    
    # Start with a reasonably large font size and decrease until it fits
    font_size = 100  # Starting font size
    font = font_size_def(font_size)
    
    while True:
        font = font_size_def(font_size)
        if not title:
            title_height = 0
        else:
            title_font = font_size_def(font_size+3)
            title_width, title_height = draw.textbbox((0, 0), title, font=title_font)[2:]
            if title_width > max_width:
                font_size -=1
                continue
        lines = text_wrap(draw, text, font, max_width)
        text_width, text_height = draw_multiline_text_size(draw, lines, font)
        total_height = title_height + text_height
        if text_width <= max_width and total_height <= max_height:
            break
        font_size -= 1  # Decrease font size and retry
        if font_size <= 0:
            raise ValueError("Cannot fit text within the given dimensions.")

    # Create the final image with the correct size
    image = Image.new('RGB', (max_width, max_height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Calculate starting y position for the text to be below the title
    total_text_height = title_height + sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines)
    y = (max_height - total_text_height) // 2
    # Draw the title if provided

    if title:
        title_width, title_height = draw.textbbox((0, 0), title, font=title_font)[2:]
        draw.text(((max_width - title_width) // 2, y), title, font=title_font, fill='black')
        y += title_height

    # Draw the text on the image
    for line in lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
        draw.text(((max_width - text_width) // 2, y), line, font=font, fill='black')
        y += text_height
    return image

# Loop der generer alle felterne
for i in range(antal_spilfelter):
    billede = ''
    felt_pos = (0,0)
    bg_farve = spil_data['farver'][i]
    felt = Image.new('RGB',felt_dims,color=bg_farve)
    tekst = spil_data['tekst'][i]
    titel = spil_data['titel'][i]
    billede_sti = spil_data['billeder'][i]
    if billede_sti != f'{mappe_navn}/':
        retning = spil_data['billede_retning'][i]
        try:
            billede = Image.open(billede_sti)
        except FileNotFoundError:
            billede = Image.open(f'{mappe_navn}/placeholder_img.jpg')
        if retning == 'LODRET':
            billede = resize_image(billede,max_width=int((felt_dims[0]/2)-40))
            if billede.width < int((felt_dims[0]/2)-40):
                max_text_width = int(felt_dims_width-billede.width-80)
            else:
                max_text_width = int((felt_dims[0]/2)-60)
            if titel != '':
               text_box = create_text_element(tekst, max_width=max_text_width, max_height=int(felt_dims[1]-40),bg_color=bg_farve, title=titel) 
            else:
                text_box = create_text_element(tekst, max_width=max_text_width, max_height=int(felt_dims[1]-40),bg_color=bg_farve) 
            felt.paste(billede,(40,20))
            felt.paste(text_box,(billede.width+80,20))
        
        else:
            if len(tekst) <=130:
                max_text_height = int((felt_dims[1]/4)-40)
                max_img_height = int(((felt_dims[1]*3)/4)-20)
            elif len(tekst) >= 350:
                max_text_height = int(((felt_dims[1]*3)/4)-40)
                max_img_height = int(((felt_dims[1])/4)-20)
            else:
                max_text_height = int((felt_dims[1]/2)-40)
                max_img_height = int((felt_dims[1]/2)-20)
            if titel != '':
               text_box = create_text_element(tekst, max_width=int(felt_dims[0]-60), max_height=max_text_height, bg_color=bg_farve, title=titel) 
            else:
                text_box = create_text_element(tekst, max_width=int(felt_dims[0]-60), max_height=max_text_height,bg_color=bg_farve) 
            billede = resize_image(billede,max_height=max_img_height)
            felt.paste(billede,(int((felt_dims[0]/2)-(billede.width/2)),20))
            felt.paste(text_box,(int(((felt_dims[0])/2)-(text_box.width/2)),int(billede.height+40)))
    
    else:
        if titel != '':
            text_box = create_text_element(tekst, max_width=int((felt_dims[0])-40), max_height=int(felt_dims[1]-40),bg_color=bg_farve, title=titel) 
        else:
            text_box = create_text_element(tekst, max_width=int((felt_dims[0])-40), max_height=int(felt_dims[1]-40),bg_color=bg_farve) 
        felt.paste(text_box,(int((felt_dims[0]/2)-(text_box.width/2)),int((felt_dims[1]-text_box.height)/2)))
    
    felter.append(felt)

pos = (pos[0]+thick_line_dim,pos[1]-felt_dims[1]-thick_line_dim)

# Flag til at få felterne til at tilføje i rækkefølge
opad_1 = True
opad_2 = False
opad_3 = False
hoejre_1 = False
hoejre_2 = False
hoejre_3 = False
nedaf_1 = False
nedaf_2 = False
nedaf_3 = False
venstre_1 = False
venstre_2 = False

# Loop der sætter alle felter ind på pladen
for felt in felter:
    spillet.paste(felt,pos)
    # Parametre, der ændrer flags så positionen for næste felt kan beregnes:
    if pos[1] < 50+thick_line_dim+felt_dims[1] and opad_1:
        opad_1 = False
        hoejre_1 = True
    if pos[0] > img_size[0]-felt_dims[0]-50-thick_line_dim*2 and hoejre_1:
        hoejre_1 = False
        nedaf_1 = True
    if pos[1] > img_size[1]-felt_dims[1]-50-thick_line_dim*2  and nedaf_1:
        nedaf_1 = False
        venstre_1 = True
    if pos[0] < 50+thick_line_dim*2+felt_dims[0]*2 and venstre_1:
        venstre_1 = False
        opad_2 = True
    if pos[1] < 50+thick_line_dim*2+felt_dims[1]*2 and opad_2:
        opad_2 = False
        hoejre_2 = True
    if pos[0] > img_size[0]-thick_line_dim*3-felt_dims[0]*2-50 and hoejre_2:
        hoejre_2 = False
        nedaf_2 = True
    if pos[1] > img_size[1]-thick_line_dim*2-felt_dims[1]*2-50 and nedaf_2:
        nedaf_2 = False
        venstre_2 = True
    if pos[0] < 50 + thick_line_dim*3+felt_dims[0]*2 and venstre_2:
        venstre_2 = False
        opad_3 = True
    if pos[1] < 50+thick_line_dim*3+felt_dims[1]*2 and opad_3:
        opad_3 = False
        hoejre_3 = True
    if pos[0] > img_size[0]-thick_line_dim*3-felt_dims[0]*3-50 and hoejre_3:
        hoejre_3 = False
        nedaf_3 = True
    
    # Ændring af position for næste felt baseret på flag
    if opad_1 or opad_2 or opad_3:
        pos = (pos[0],pos[1]-felt_dims[1]-thin_line_dim)
    elif hoejre_1 or hoejre_2 or hoejre_3:
        pos = (pos[0]+thin_line_dim+felt_dims[0],pos[1])
    elif nedaf_1 or nedaf_2 or nedaf_3:
        pos = (pos[0],pos[1]+felt_dims[1]+thin_line_dim)
    elif venstre_1 or venstre_2:
        pos = (pos[0]-thin_line_dim-felt_dims[0],pos[1])

# Indsættelse af regelsættet i midten
# Try if center img is in dir, else use placeholder
try:
    center_img = Image.open(center_img_sti)
except FileNotFoundError:
    center_img = Image.open(f'{mappe_navn}/placeholder_img.jpg')

# Resize, så det passer i midten af pladen
center_img_sized = center_img.resize((4584, 4323), Image.LANCZOS)
spillet.paste(center_img_sized,(int(50+thick_line_dim*2+thin_line_dim*3+felt_dims_width*3),int(50+thick_line_dim*2+thin_line_dim*3+felt_dims_height*3)))

# Linjerne der angiver spilleretningningen
spillet_gen.line([(50+thick_line_dim+felt_dims_width,img_size[1]-50),(50+thick_line_dim+felt_dims_width,50+thick_line_dim+felt_dims_height),(img_size[0]-50-thick_line_dim*2-felt_dims_width,50+thick_line_dim+felt_dims_height),(img_size[0]-50-thick_line_dim*2-felt_dims_width,img_size[1]-50-thick_line_dim-felt_dims_height),(50+thick_line_dim*2+felt_dims_width*2,img_size[1]-50-thick_line_dim-felt_dims_height),(50+thick_line_dim*2+felt_dims_width*2,50+thick_line_dim*2+felt_dims_height*2),(img_size[0]-50-thick_line_dim*2-felt_dims_width*2,50+thick_line_dim*2+felt_dims_height*2),(img_size[0]-50-thick_line_dim*2-felt_dims_width*2,img_size[1]-50-thick_line_dim*2-felt_dims_height*2),(50+thick_line_dim*2+felt_dims_width*3,img_size[1]-50-thick_line_dim*2-felt_dims_height*2)],fill='black',width=thick_line_dim+15) 

# Gem spillet som JPG-fil med det indtastede navn
spillet.save(f'exports/{spil_navn}.png',dpi=(300,300))