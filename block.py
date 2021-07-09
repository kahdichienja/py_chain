import json
import os
import hashlib
from typing import Dict, Any


BLOCKDIR = 'blockchain/'

def get_hash(prev_block):
    with open(BLOCKDIR + prev_block, 'rb') as f:
        content = f.read()


    return hashlib.md5(content).hexdigest()

def dict_hash(dictionary: Dict[str, Any]) -> str:
    dhash = hashlib.md5()
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


def hash_block(content):
    return hashlib.sha256(content).hexdigest() #hashlib.md5(content).hexdigest()

def get_finger_print_data(hash_finger_pring):

    files = sorted(os.listdir(BLOCKDIR), key=lambda x: int(x))
    chained_data = []
    for file in files[1:]:
        # open file
        with open(BLOCKDIR + file) as f:
            block = json.load(f)
        # block_data = block.get("data")
        hashed_data = block.get("prev_block").get("hash")
        doc_hash = block.get("doc_hash")
        prev_file_name = block.get("prev_block").get("file_name")
        actual_hash = get_hash(prev_file_name)

        if(hashed_data == actual_hash):
            res = "True"
            if hash_finger_pring == doc_hash:
                chained_data.append({"block": prev_file_name, "valid": res, "chained_data": block})
        else:
            res = "false"
            if hash_finger_pring == doc_hash:
                chained_data.append({"block": prev_file_name, "valid": res, "chained_data": block})
            chained_data.append({"block": prev_file_name, "valid": res, "chained_data": block})
        
    return chained_data

def check_integrity():
    files = sorted(os.listdir(BLOCKDIR), key=lambda x: int(x))

    results = []


    for file in files[1:]:
        with open(BLOCKDIR + file) as f:
            block = json.load(f)
        prev_hash = block.get("prev_block").get("hash")
        # block_data = block.get("data")
        prev_file_name = block.get("prev_block").get("file_name")

        actual_hash = get_hash(prev_file_name)
        if(prev_hash == actual_hash):
            res = "True"
        else:
            res = "false"
        

        # print(f"Block {prev_file_name}: {res}")
        # results.append({"block": {prev_file_name}, "result": {res}, "data": block_data})
        # results.append({"data": block_data})

        results.append({"block": prev_file_name, "valid": res, "chained_data": block})


    return results



def write_block(
    student_name,
    id_number,
    kra_pin,
    email_address,
    huduma_number,
    profile_url,
    institution_name,
    institution_id,
    date_of_graduation,
    course,
    file_url,
    verified=False,
):
    blocks_count = len(os.listdir(BLOCKDIR)) 
    prev_block = str(blocks_count)
    data = {
        "data": {
            "student_datails": {
                "name": student_name,
                "id_number": id_number,
                "kra_pin": kra_pin,
                "email_address": email_address,
                "huduma_number": huduma_number,
                "profile_url": profile_url,
            },
            "accademic_details": {
                "institution_name": institution_name,
                "institution_id": institution_id,
                "date_of_graduation": date_of_graduation,
                "course": course,
            },
            "accademic_paper": {"file_url": file_url, "verified": verified},
        },

        "prev_block": {"hash": get_hash(prev_block), "file_name": prev_block},
    }

    generate_hash = dict_hash(dictionary = data)

    data.update({"doc_hash": generate_hash})

    current_block = BLOCKDIR + str(blocks_count + 1)

    with open(current_block, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False) 
        f.write("\n")


def main():
    # write_block(
    #     student_name="Mavine Wechul Musin",
    #     id_number=133124,
    #     kra_pin=213412,
    #     email_address="mavo@g.net",
    #     huduma_number=12021124,
    #     profile_url="https://cdn4.vectorstock.com/i/1000x1000/40/83/hacker-icon-on-white-background-flat-style-vector-26994083.jpg",
    #     institution_name="Rongo University",
    #     institution_id=1,
    #     date_of_graduation="123124",
    #     course="Computer Science",
    #     file_url="https://docs.google.com/document/d/1WyenTEXXFzDvE66o5N7KHIeCIXZmwFfCRvON8ZuRisM/edit",
    #     verified=False,
    # )

    # res = check_integrity()
    res = get_finger_print_data(hash_finger_pring = "319f463156c2a6c8aa90535a3260a7a5")
    

    print(res)


if __name__ == "__main__":
    main()
