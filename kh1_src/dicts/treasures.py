# Courtesy of the KH1FM Randomizer team
def treasure_dicts(obj):
    # For now it reflects FM
    # I havw to research vanilla differences
    obj.treasure_dicts = {
        "Dive to the Heart": {
            # Ironically on the last byte of the array and the highest used bit
            "Awakening: Potion": 0x1FC2,
        },
        "Destiny Islands": {
            "Protect Chain Chest": 0x0000,
        },
        "Traverse Town": {
            "Candle Puzzle: Defense Up": 0x0140,
            "Accessory Shop's Roof: Postcard": 0x0141,
            "Boots and Shoes Awning: Postcard": 0x0142,
            "2nd District Rooftop: Mythril Shard": 0x0143,
            "Gizmo Shop Facade: Mega-Potion": 0x0180,
            "Alleyway Balcony: Potion": 0x0181,
            "Alleyway Blue Room Awning: Pretty Stone": 0x0182,
            "Alleyway Corner: Potion": 0x0183,
            # "Unused": 0x01C0,
            "Green Room Clock Puzzle: Mythril": 0x01C1,
            "Green Room Table: Elixir": 0x01C2,
            "Red Room: Pretty Stone": 0x01C3,
            "Mystical House Yellow Trinity: AP Up": 0x0200,
            "Accessory Shop: Mythril Shard": 0x0201,
            "Secret Waterway White Trinity: Orichalcum": 0x0202,
            "Geppetto's House: Wishing Star": 0x0203,
            "Item Workshop Right: Mythril Shard": 0x0240,
            "1st District Blue Trinity Balcony: Postcard": 0x0280,
            "Mystical House Glide: Dalmatians 1, 2, 3": 0x0580,
            "Alleyway Behind Crates: Dalmatians 4, 5, 6": 0x581,
            "Item Workshop Left: Dalmatians 7, 8, 9": 0x0582,
            "Secret Waterway Stairs: Dalmatians 10, 11, 12": 0x0583,
        },
        "Wonderland": {
            "Rabbit Hole Green Trinity: ": 0x05C0,
            "Rabbit Hole Heartless Wave 1: ": 0x05C1,
            "Rabbit Hole Heartless Wave 2: ": 0x05C2,
            "Rabbit Hole Heartless Wave 3: ": 0x05C3,
        },
        "Deep Jungle": {
            
        },
        "Hundred Acre Woods": {
            "Meadow Inside Log: ": 0x0A43,
            "Bouncing Spot Cliff: ": 0x0A80,
            "Bouncing Spot Tree Alcove: ": 0x0A80,
            "Bouncing Spot Giant Pot: ": 0x0A80,
        },
        "Agrabah": {
            
        },
        "Monstro": {
            "Mouth Boat Deck: High Jump": 0x1583,
        },
        "Atlantica": {
            "Sunken Ship In Flipped Boat: Elixir": 0x0FC0,
            "Sunken Ship Seabed: Mythril Shard": 0x0FC1,
            "Below Deck: Mythril Shard": 0x0FC2,
            "Ariel's Grotto High: Torn Page": 0x0FC3,
            "Ariel's Grotto Middle: Cottage": 0x1000,
            "Ariel's Grotto Low: Mega-Potion": 0x1001,
            "Ursula's Lair: Mythril": 0x1002,
            "Large Chest: Orichalcum": 0x1003,
            "Triton's Palace White Trinity: Orichalcum": 0x1040,
        },
        "Neverland": {
            "Deck White Trinity: ": 0x1781,
        },
        "Hollow Bastion": {
            
        },
        "End of the World": {
            
        },
    }
    obj.clam_dict = {
        "Undersea Gorge Blizzard Clam": 0x00,
        "Undersea Gorge Ocean Floor Clam": 0x01,
        "Undersea Valley Higher Cave Clam": 0x02,
        "Undersea Valley Lower Cave Clam": 0x03,
        "Undersea Valley Fire Clam": 0x04,
        "Undersea Valley Wall Clam": 0x05,
        "Undersea Valley Pillar Clam": 0x06,
        "Undersea Valley Ocean Floor Clam": 0x07,
        "Triton's Palace Thunder Clam": 0x10,
        "Triton's Palace Wall Right Clam": 0x11,
        "Triton's Palace Near Path Clam": 0x12,
        "Triton's Palace Wall Left Clam": 0x13,
        "Triton's Palace Cavern Nook Clam": 0x14,
        "Triton's Palace Below Deck Clam": 0x15,
        "Triton's Palace Undersea Garden Clam": 0x16,
        "Triton's Palace Undersea Cave Clam": 0x17,
    }
    obj.bigben_dict = {
        "01:00 Door": 0x07,
        "02:00 Door": 0x06,
        "03:00 Door": 0x05,
        "04:00 Door": 0x04,
        "05:00 Door": 0x03,
        "06:00 Door": 0x02,
        "07:00 Door": 0x01,
        "08:00 Door": 0x00,
        "09:00 Door": 0x17,
        "10:00 Door": 0x16,
        "11:00 Door": 0x15,
        "12:00 Door": 0x14,
    }
