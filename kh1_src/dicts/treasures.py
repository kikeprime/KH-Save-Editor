# Courtesy of the KH1FM Randomizer team
def treasure_dicts(obj):
    # For now it reflects FM
    # I havw to research vanilla differences
    @property
    def treasure_chests(self):
        item_0200 = "Power Up"
        item_0640 = "Dalmatians 13, 14, 15"
        item_0641 = "Aero-G"
        item_0642 = "Dalmatians 58, 59, 60"
        item_0643 = "Shell-G"
        item_0680 = "Thundara-G"
        item_0783 = "Protera Chain"
        item_1501 = "Firaga-G"
        item_1502 = "Holy-G"
        item_17C1 = "Dispel-G"
        # Hollow Bastion
        item_1980 = "Dispel-G"
        item_19C3 = "Holy-G"
        item_1A41 = "Power Up"
        item_1AC1 = "Float-G 2"
        item_1B40 = "Flare-G"
        item_1B42 = "Float-G 2"
        item_1B43 = "Float-G 1"
        item_1BC3 = "Flare-G"
        # End of the World
        item_1C40 = "Power Up"
        item_1C41 = "Defense Up"
        item_1C42 = "Megalixir"
        item_1C43 = "Omega Arts"
        item_1C80 = "Angel Bangle"
        item_1C81 = "Megalixir"
        item_1C82 = "Defense Up"
        item_1C83 = "Three Stars"
        item_1CC0 = "Power Up"
        item_1CC1 = "Dark Ring"
        item_1CC2 = "Thundara-G"
        item_1CC3 = "Ultima-G"
        item_1D00 = "Haste-G"
        item_1D01 = "Haste2-G"
        item_1D02 = "Esuna-G"
        item_1D03 = "Brave Warrior"
        item_1D40 = "Ifrit's Horn"
        item_1D41 = "Inferno Band"
        item_1D42 = "White Fang"
        item_1D43 = "Ray of Light"
        item_1D81 = "Holy Circlet"
        item_1D82 = "Raven's Claw"
        item_1DC0 = "Megalixir"
        if hasattr(self, "fm") and self.fm:
            item_0200 = "AP Up"
            item_0640 = "Thundara-G"
            item_0641 = "Dalmatians 13, 14, 15"
            item_0642 = "Meteor-G"
            item_0643 = "Thundara-G"
            item_0680 = "Dalmatians 58, 59, 60"
            item_0783 = "Protect Chain"
            item_1501 = "Holy-G"
            item_1502 = "Shiva Belt"
            item_17C1 = "Meteor-G"
            # Hollow Bastion
            item_1980 = "Meteor-G"
            item_19C3 = "Haste2-G"
            item_1A41 = "AP Up"
            item_1AC1 = "Royal Crown"
            item_1B40 = "Dark Matter"
            item_1B42 = "Ultima-G"
            item_1B43 = "Thundaga-G"
            item_1BC3 = "Dark Matter"
            # End of the World
            item_1C40 = "Mythril Shard"
            item_1C41 = "Pretty Stone"
            item_1C42 = "Mega-Potion"
            item_1C43 = "Mythril"
            item_1C80 = "Elixir"
            item_1C81 = "Mythril Shard"
            item_1C82 = "Pretty Stone"
            item_1C83 = "Cottage"
            item_1CC0 = "Gale"
            item_1CC1 = "AP Up"
            item_1CC2 = "Full-Life-G"
            item_1CC3 = "Meteor Strike"
            item_1D00 = "Drill-G"
            item_1D01 = "Dark Matter"
            item_1D02 = "Ultima-G"
            item_1D03 = "Spirit Gem"
            item_1D40 = "Thunder Gem"
            item_1D41 = "Frost Gem"
            item_1D42 = "Bright Gem"
            item_1D43 = "Blaze Gem"
            item_1D81 = "Lucid Gem"
            item_1D82 = "Mighty Shield"
            item_1DC0 = "Elixir"
        return {
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
                "Green Room Clock Puzzle: Mythril": 0x01C1,
                "Green Room Table: Elixir": 0x01C2,
                "Red Room: Pretty Stone": 0x01C3,
                f"Mystical House Yellow Trinity: {item_0200}": 0x0200,
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
                "Rabbit Hole Green Trinity: Elixir": 0x05C0,
                "Rabbit Hole Heartless Wave 1: Camping Set": 0x05C1,
                "Rabbit Hole Heartless Wave 2: Mega-Potion": 0x05C2,
                "Rabbit Hole Heartless Wave 3: Megalixir": 0x05C3,
                "Bizarre Room Green Trinity: Mythril Shard": 0x0600,
                f"Queen's Castle Left Red Chest: {item_0640}": 0x0640,
                f"Queen's Castle Right Blue Chest: {item_0641}": 0x0641,
                f"Queen's Castle Right Red Chest: {item_0642}": 0x0642,
                f"Lotus Forest Thunder Plant: {item_0643}": 0x0643,
                f"Lotus Forest Painting Thunder Plant: {item_0680}": 0x0680,
                "Lotus Forest With Glide: Orichalcum": 0x0681,
                "Lotus Forest Nut: Dalmatians 16, 17, 18": 0x0682,
                "Lotus Forest Corner: Scan-G": 0x0683,
                "Bizarre Room Lamp: Defense Up": 0x06C0,
                "Tea Party Garden Left: Flare-G": 0x06C2,
                "Tea Party Garden Right: Dalmatians 19, 20, 21": 0x06C3,
                "Tea Party Garden Balcony: Dark Matter": 0x0700,
                "Tea Party Garden Corner: Mythril": 0x0701,
                "Lotus Forest White Trinity: Lady Luck": 0x0702,
            },
            "Deep Jungle": {
                "Tree House Beneath Tree House: Mega-Potion": 0x0782,
                f"Tree House Rooftop: {item_0783}": 0x0783,
                "Hippo's Lagoon Center: Dalmatians 25, 26, 27": 0x07C0,
                "Hippo's Lagoon Left: Mega-Potion": 0x07C1,
                "Hippo's Lagoon Right: Meteor-G": 0x07C2,
                "Vines: Dalmatians 28, 29, 30": 0x0800,
                "Vines 2: Mythril": 0x0801,
                "Climbing Trees Blue Trinity: Thundara-G": 0x0802,
                "Tunnel: Mega-Ether": 0x0840,
                "Cavern of Hearts White Trinity: Orichalcum": 0x0841,
                "Camp Blue Trinity: Dalmatians 34, 35, 36": 0x0842,
                "Tent: Mythril Shard": 0x0843,
                "Waterfall Cavern Low: Mythril Shard": 0x0880,
                "Waterfall Cavern Middle: Dalmatians 31, 32, 33": 0x0881,
                "Waterfall Cavern High Wall: Mythril": 0x0882,
                "Waterfall Cavern High Middle: Orichalcum": 0x0883,
                "Cliff Left: Mega-Potion": 0x08C0,
                "Cliff Right: Mythril Shard": 0x08C1,
                "Tree House Suspended Boat: Mythril": 0x08C2,
            },
            "Hundred Acre Woods": {
                "Meadow Inside Log: Mythril Shard": 0x0A43,
                "Bouncing Spot Cliff: Mythril Shard": 0x0A80,
                "Bouncing Spot Tree Alcove: Dark Matter": 0x0A80,
                "Bouncing Spot Giant Pot: AP Up": 0x0A80,
            },
            "Agrabah": {
                "Plaza By Storage: Mega-Potion": 0x0C41,
                "Plaza Raised Terrace: Mega-Ether": 0x0C42,
                "Plaza Top Corner: Cottage": 0x0C43,
                "Alley: Mega-Potion": 0x0C80,
                "Bazaar Across Windows: Thundara-G": 0x0C81,
                "Bazaar High Corner: Fire Ring": 0x0C82,
                "Main Street Right: Mega-Ether": 0x0C83,
                "Main Street Alley: Dark Matter": 0x0CC0,
                "Main Street Palace Gates: Mythril": 0x0CC1,
                "Palace Gates Low: Protera Chain": 0x0CC2,
                "Palace Gates High Opposite: Dalmatians 52, 53, 54": 0x0CC3,
                "Palace Gates High Close: Osmose-G": 0x0D00,
                "Storage Green Trinity: AP Up": 0x0D01,
                "Storage Behind Barrel: Mega-Potion": 0x0D02,
                "Cave of Wonders Left: Mega-Ether": 0x0D03,
                "Cave of Wonders Tall Tower: Dalmatians 49, 50, 51": 0x0D40,
                "Hall High Left: Elixir": 0x0D41,
                "Hall Near Bottomless Hall: Mythril Shard": 0x0D42,
                "Bottomless Hall Raised Platform: Cottage": 0x0D43,
                "Bottomless Hall Pillar: Elixir": 0x0D80,
                "Bottomless Hall Across Chasm: Mega-Potion": 0x0D81,
                "Treasure Room Across Platforms: Dalmatians 37, 38, 39": 0x0D82,
                "Treasure Room Small Pile: Mythril Shard": 0x0D83,
                "Treasure Room Large Pile: Thundaga-G": 0x0DC0,
                "Treasure Room Above Fire: Defense Up": 0x0DC1,
                "Relic Chamber Jump from Stairs: Mythril": 0x0DC2,
                "Relic Chamber Stairs: Thunder Ring": 0x0DC3,
                "Dark Chamber Abu Gem: Protera Chain": 0x0E00,
                "Dark Chamber Across Entrance: Meteor-G": 0x0E01,
                "Dark Chamber Bridge: Torn Page": 0x0E02,
                "Dark Chamber Save Point: Cottage": 0x0E03,
                "Silent Chamber Blue Trinity: Thundara-G": 0x0E40,
                "Hidden Room Right: Haste2-G": 0x0E41,
                "Hidden Room Left: Dalmatians 46, 47, 48": 0x0E42,
                "Aladdin's House Main Street: Scissors-G": 0x0E43,
                "Aladdin's House Plaza: Megalixir": 0x0E40,
                "Cave of Wonders White Trinity: Ifrit Belt": 0x0E41,
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
            "Halloween Town": {
                "Moonlight Hill White Trinity: Dalmatians 67, 68, 69": 0x12C3,
                "Bridge Under Bridge: Flare-G": 0x1300,
                "Boneyard Tombstone Puzzle: Jack-In-The-Box": 0x1301,
                "Bridge Right of Gate: Defense Up": 0x1302,
                "Cemetery Behind Grave: Dark Matter": 0x1303,
                "Cemetery By Cat Shape: Dalmatians 64. 65. 66": 0x1340,
                "Cemetery Between Graves: Scissors-G": 0x1341,
                "Oogie's Manor Lower Iron Cage: Orichalcum": 0x1342,
                "Oogie's Manor Upper Iron Cage: Mega-Ether": 0x1343,
                "Oogie's Manor Hollow: Dalmatians 40, 41, 42": 0x1380,
                "Oogie's Manor Red Trinity: Mythril Shard": 0x1381,
                "Guillotine Square Tower: Power Up": 0x1382,
                "Guillotine Pumpkin Left: Elixir": 0x1383,
                "Oogie's Manor Entrance Steps: Ether": 0x13C0,
                "Oogie's Manor Inside Entrance: Ether": 0x13C1,
                "Bridge Left of Gate: Meteor-G": 0x1480,
                "Cemetery Striped Grave: Holy-G": 0x1481,
                "Guillotine Square Under Stairs: Thundara-G": 0x1482,
                "Guillotine Pumpkin Right: Dalmatians 70, 71, 72": 0x1483,
            },
            "Olympus Coliseum": {
                "Left Pillars: Mega-Potion": 0x14C1,
                "Right Blue Trinity: Dalmatians 22, 23, 24": 0x14C2,
                "Left Blue Trinity: Mythril Shard": 0x14C3,
                "White Trinity: Violetta": 0x1500,
                f"Blizzara Puzzle: {item_1501}": 0x1501,
                f"Blizzaga Puzzle: {item_1502}": 0x1502,
            },
            "Monstro": {
                "Mouth Boat Deck: High Jump": 0x1583,
                "Mouth Platform Boat Side: Cottage": 0x15C0,
                "Mouth Platform Across from Boat: Dalmatians 73, 74, 75": 0x15C1,
                "Mouth Near Ship: Scan-G": 0x15C2,
                "Mouth Green Trinity: Mythril Shard": 0x15C3,
                "Chamber 2 Ground: Cottage": 0x1603,
                "Chamber 2 Platform: Megalixir": 0x1640,
                "Chamber 5 Platform: Mythril": 0x1682,
                "Chamber 3 Ground: Mega-Ether": 0x1683,
                "Chamber 3 Platform Above Chamber 2: Dalmatians 55, 56, 57": 0x16C0,
                "Chamber 3 Near Chamber 6: Osmose-G": 0x16C1,
                "Chamber 3 Platform Near Chamber 6: Flare-G": 0x16C2,
                "Mouth Near Teeth: Watergleam": 0x1741,
                "Chamber 5 Atop Barrel: Dalmatians 79, 80, 81": 0x1742,
                "Chamber 5 Low 2nd: Mega-Ether": 0x1743,
                "Chamber 5 Low 1st: Thundaga-G": 0x1780,
                # I broke my order rule a bit here
                "Chamber 6 Platform: Megalixir": 0x0F02,
                "Chamber 6 Platform Near Chamber 5: Torn Page": 0x0F03,
                "Chamber 6 Raised Area: Mythril": 0x0F40,
                "Chamber 6 Low: Dalmatians 76, 77, 78": 0x0F41,
                "Chamber 6 White Trinity: Dark Matter": 0x1FC1,
            },
            "Neverland": {
                "Deck White Trinity: Dalmatians 43, 44, 45": 0x1781,
                "Crow's Nest: Orichalcum": 0x1782,
                "Hold Right Yellow Trinity: Orichalcum": 0x1783,
                "Hold Left Yellow Trinity: Dark Matter": 0x17C0,
                f"Galley: {item_17C1}": 0x17C1,
                "Cabin: Protera Chain": 0x17C2,
                "Hold Flight 1st: Dalmatians 82, 83, 84": 0x17C3,
                "Clock Tower: Flare-G": 0x1903,
                "Hold Flight 2nd: Paper-G": 0x1940,
                "Hold Yellow Trinity Green Chest: Dalmatians 85, 86, 87": 0x1941,
                "Captain's Cabin: Dalmatians 88, 89, 90": 0x1942,
            },
            "Hollow Bastion": {
                "Rising Falls Water's Surface: Life-G": 0x1943,
                f"Rising Falls Under Water 1st: {item_1980}": 0x1980,
                "Rising Falls Under Water 2nd: Defense Up": 0x1981,
                "Rising Falls Platform Near Save Point: Dalmatians 91, 92, 93": 0x1982,
                "Rising Falls Platform Near Bubble: Blizzara Ring": 0x1983,
                "Rising Falls High Platform: Megalixir": 0x19C0,
                "Castle Gates Gravity: Dalmatians 94, 95, 96": 0x19C1,
                "Castle Gates Freestanding Pillar: Orichalcum": 0x19C2,
                f"Castle Gates High Pillar: {item_19C3}": 0x19C3,
                "Great Crest Lower: Orichalcum": 0x1A00,
                "Great Crest Platform: Thundaga-G": 0x1A01,
                "High Tower 2nd Gravity: Osmose-G": 0x1A02,
                "High Tower 1st Gravity: Thundara Ring": 0x1A03,
                "High Tower Above Sliding Blocks: Megalixir": 0x1A40,
                f"Entrance Hall Left of Emblem Door: {item_1A41}": 0x1A41,
                "Library Top of Bookshelf: Ultima-G": 0x1A42,
                "Library Ground Floor Carousel: Elixir": 0x1A43,
                "Library Top of Bookshelf Carousel: AP Up": 0x1A80,
                "Library 1st Floor Carousel 1st: Mythril": 0x1A81,
                "Library 1st Floor Carousel 2nd: Mega-Potion": 0x1A82,
                "Lift Stop Gravity 2nd: Ramuh Belt": 0x1A83,
                "Lift Stop Gravity 1st: Osmose-G": 0x1AC0,
                f"Lift Stop Under Sliding Blocks: {item_1AC1}": 0x1AC1,
                "Lift Stop Outside Library Gravity: Dalmatians 97, 98, 99": 0x1AC2,
                "Lift Stop Heartless Sigil Door Gravity: Orichalcum": 0x1AC3,
                "Base Level Bubble Under the Wall Platform: Mythril": 0x1B00,
                "Base Level Platform Near Entrance: Paper-G": 0x1B01,
                "Base Level Near Crystal Switch: Thundara-G": 0x1B02,
                "Waterway Near Save Point: Fira Ring": 0x1B03,
                f"Waterway Blizzard on Bubble: {item_1B40}": 0x1B40,
                "Waterway Unlock Passage: Thundaga-G": 0x1B41,
                f"Dungeon By Candles Chest: {item_1B42}": 0x1B42,
                f"Dungeon Corner Chest: {item_1B43}": 0x1B43,
                f"Grand Hall Steps Right Side: {item_1BC3}": 0x1BC3,
                "Grand Hall Oblivion Chest": 0x1C00,
                "Grand Hall Left of Gate: Dalmatians 61, 62, 63": 0x1C01,
                "Entrance Hall Push the Statue: Emblem Piece": 0x1C02,
                "Rising Falls White Trinity: Thundaga-G": 0x1C03,
            },
            "End of the World": {
                f"Final Dimension 1st: {item_1C40}": 0x1C40,
                f"Final Dimension 2nd: {item_1C41}": 0x1C41,
                f"Final Dimension 3rd: {item_1C42}": 0x1C42,
                f"Final Dimension 4th: {item_1C43}": 0x1C43,
                f"Final Dimension 5th: {item_1C80}": 0x1C80,
                f"Final Dimension 6th: {item_1C81}": 0x1C81,
                f"Final Dimension 7th: {item_1CC0}": 0x1CC0,
                f"Final Dimension 8th: {item_1CC1}": 0x1CC1,
                f"Final Dimension 9th: {item_1C83}": 0x1C83,
                f"Final Dimension 10th: {item_1C82}": 0x1C82,
                f"Giant Crevasse 1st: {item_1D00}": 0x1D00,
                f"Giant Crevasse 2nd: {item_1D02}": 0x1D02,
                f"Giant Crevasse 3rd: {item_1CC2}": 0x1CC2,
                f"Giant Crevasse 4th: {item_1D01}": 0x1D01,
                f"Giant Crevasse 5th: {item_1CC3}": 0x1CC3,
                f"Traverse Town: {item_1D03}": 0x1D03,
                f"Wonderland: {item_1D40}": 0x1D40,
                f"Olympus Coliseum: {item_1D41}": 0x1D41,
                f"Deep Jungle: {item_1D42}": 0x1D42,
                f"Agrabah: {item_1D43}": 0x1D43,
                "Atlantica: AP Up": 0x1D80,
                f"Halloween Town: {item_1D81}": 0x1D81,
                f"Neverland: {item_1D82}": 0x1D82,
                f"Hundred Acre Woods: Megalixir": 0x1D83,
                f"Hollow Bastion: {item_1DC0}": 0x1DC0,
                "Final Rest: Megalixir": 0x1DC1,
            },
        }
    type(obj).treasure_dicts = treasure_chests
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
        "Cavern Nook Clam": 0x14,
        "Below Deck Clam": 0x15,
        "Undersea Garden Clam": 0x16,
        "Undersea Cave Clam": 0x17,
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
