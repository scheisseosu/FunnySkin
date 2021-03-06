import sys,os,shutil

if __name__ == "__main__":
    args = sys.argv

    fp = input("Enter the path to your osu! installation folder: ")
    fp = os.path.realpath(fp)

    if not os.path.basename(fp) == "Skins":
        fp = os.path.join(fp,"Skins")
    
    if not os.path.exists(fp):
        print(f"Error: path to Skins folder does not exist\n\t{fp}")
        sys.exit(0)
    
    os.chdir(fp)
    folders = []
    for root,dirs,files in os.walk(os.getcwd()):
        for skin_fold in dirs:
            full_dir = os.path.join(root,skin_fold)

            #Check is valid skin
            if not os.path.isfile(os.path.join(full_dir,"skin.ini")):
                continue #skin this folder
            
            #Skip if already listing skin with same name
            if skin_fold in folders:
                continue
            
            folders.append(skin_fold)
            i = folders.index(skin_fold)
            print(f"{i}\t{skin_fold}")
    
    choice = input("Select skin to make funnier: ")
    #catch non-digit input
    if not choice.isdigit():
            choice = -1
    else:
        #typecast
        choice = int(choice)

    while (choice<0 or choice>=len(folders)):
        choice = input("Invalid selection. Enter a number corresponding to the skin selections above: ")
        #catch non-digit input
        if not choice.isdigit():
            choice = -1
            continue
        else:
            #typecast
            choice = int(choice)
    
    skin = folders[int(choice)]
    selected = os.path.join(fp,skin)

    #copy folder
    new_name = skin+" BUT FUNNIER"
    dest = os.path.join(fp,new_name)

    try:
        new_fp = shutil.copytree(selected,dest)
    except FileExistsError:
        print(f"Folder for name {dest} already exists, likely because program was already run. Delete or rename this folder and try again.")
        sys.exit(0)
    os.chdir(new_fp)
    ini_fp = os.path.join(os.getcwd(),"skin.ini")
    with open(ini_fp,"r") as f:
        lines = f.readlines()
        hitc_location = os.getcwd()
        naming_form = "default"
        for l in lines:
            if "HitCirclePrefix" in l:
                #skin.ini defines a custom hitcircle font location; use this as hitc_location
                defined = l.split(": ")[-1]

                #if location is default, stay in main skin folder
                if defined.strip() == "default":
                    break
                
                #get tail
                dirname,naming_form = os.path.split(defined)
                hitc_location = os.path.join(os.getcwd(),dirname)
                break
        
        #Tail of hitc_location is the base name of every image
        print(f"Found hitcircle numbers at {hitc_location} with naming {naming_form}, now editing...")
        os.chdir(hitc_location)

        #walk dir
        elems = []
        for root,dirs,files in os.walk(os.getcwd()):
            #for file in folder
            for f in files:
                if not f.startswith(naming_form):
                    #not a combo number
                    continue
                elems.append(f)

        #loop through nums
        for e in elems:
            num = int(e[len(naming_form)+1])

            #skip 2 and 7 elems
            if num==2 or num==7:
                continue
            

            new_num = 2
            #set new number to 7 for odds
            if num%2 == 1:
                new_num = 7
            
            #get source filename based on format of e (catches @2x versions)
            copy_src = f"{naming_form}-{new_num}{e[len(naming_form)+2:]}"
            #print(f"Copying {copy_src} into {e}")

            if not os.path.isfile(copy_src):
                #2/7 file corresponding to this element does not exist; skip
                continue

            #copy 2 or 7 into the current element
            shutil.copy(copy_src,e)
        
        print("Conversion complete!")

            

        



            