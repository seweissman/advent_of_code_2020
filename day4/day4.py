"""
You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your passport. While these documents are extremely similar, North Pole Credentials aren't issued by a country and therefore aren't actually valid documentation for travel in most of the world.

It seems like you're not the only one having problems, though; a very long line has formed for the automatic passport scanners, and the delay could upset your travel itinerary.

Due to some questionable network security, you realize you might be able to solve both of these problems at the same time.

The automatic passport scanners are slow because they're having trouble detecting which passports have all required fields. The expected fields are as follows:

byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)
Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of key:value pairs separated by spaces or newlines. Passports are separated by blank lines.

Here is an example batch file containing four passports:

ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
The first passport is valid - all eight fields are present. The second passport is invalid - it is missing hgt (the Height field).

The third passport is interesting; the only missing field is cid, so it looks like data from North Pole Credentials, not a passport at all! Surely, nobody would mind if you made the system temporarily ignore missing cid fields. Treat this "passport" as valid.

The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other field is not, so this passport is invalid.

According to the above rules, your improved system would report 2 valid passports.

Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file, how many passports are valid?

--- Part Two ---
The line is moving more quickly now, but you overhear airport security talking about how passports with invalid data are getting through. Better add some data validation, quick!

You can continue to ignore the cid field, but each other field has strict rules about what values are valid for automatic validation:

byr (Birth Year) - four digits; at least 1920 and at most 2002.
iyr (Issue Year) - four digits; at least 2010 and at most 2020.
eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
hgt (Height) - a number followed by either cm or in:
If cm, the number must be at least 150 and at most 193.
If in, the number must be at least 59 and at most 76.
hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
pid (Passport ID) - a nine-digit number, including leading zeroes.
cid (Country ID) - ignored, missing or not.
Your job is to count the passports where all required fields are both present and valid according to the above rules. Here are some example values:

"""
# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)
import re
VALID_KEYS = {"byr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}
def is_valid_passport1(passport):
    passport_fields = [field[0:field.index(":")] for field in passport.split()]
    if len(passport_fields) == 8:
        return True
    if len(passport_fields) == 7 and "cid" not in passport_fields:
        return True
    return False

def is_valid_passport2(passport):
    """
    """
    passport_fields = [field.split(":") for field in passport.split()]
    passport_fields = dict(passport_fields)
    if len(passport_fields) < 7:
        return False
    if len(passport_fields) == 7 and "cid" in passport_fields:
        return False
    #     byr (Birth Year) - four digits; at least 1920 and at most 2002.
    byr = int(passport_fields["byr"])
    if not (1920 <= byr <= 2002):
        return False

    #     iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    iyr = int(passport_fields["iyr"])
    if not (2010 <= iyr <= 2020):
        return False

    #     eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    eyr = int(passport_fields["eyr"])
    if not (2020 <= eyr <= 2030):
        return False
    #     hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    hgt = passport_fields["hgt"]
    m = re.match(r"(^\d+)(cm|in)$", hgt)
    if m is None:
        return False
    val = int(m.group(1))
    unit = m.group(2)
    if unit == "cm":
        if not (150 <= val <= 193):
            return False
    elif unit == "in":
        if not(59 <= val <= 76):
            return False
    #     hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    hcl = passport_fields["hcl"]
    m = re.match(r"^#[0-9a-f]{6}$", hcl)
    if m is None:
        return False
    #     ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    ecl = passport_fields["ecl"]
    if not ecl in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
        return False
    #     pid (Passport ID) - a nine-digit number, including leading zeroes.
    pid = passport_fields["pid"]
    m = re.match(r"^\d{9}$", pid)
    if m is None:
        return False
    #     cid (Country ID) - ignored, missing or not.
    return True


if __name__ == "__main__":
    valid_passport1_ct = 0
    valid_passport2_ct = 0
    with open("input.txt") as input:
        passport = ""
        for line in input.readlines():
            line = line.strip()
            print("line: ", line)
            if len(passport) > 0 and passport[-1] != " ":
                passport += " "
            passport += line
            if line == "":
                if len(passport) > 0:
                    if is_valid_passport1(passport):
                        valid_passport1_ct += 1
                    if is_valid_passport2(passport):
                        print(">>>", passport, "<<<")
                        valid_passport2_ct += 1
                    passport = ""
        if len(passport) > 0:
            if is_valid_passport1(passport):
                valid_passport1_ct += 1
            if is_valid_passport2(passport):
                print(">>>", passport, "<<<")
                valid_passport2_ct += 1
    print(valid_passport1_ct)
    print(valid_passport2_ct)

