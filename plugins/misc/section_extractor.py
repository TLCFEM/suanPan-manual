#  Copyright (C) 2022-2025 Theodore Chang
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Extracts and processes structural steel section properties from the AISC Shapes Database Excel file.

This script downloads the AISC shapes database, filters for specific section types (WT, MT, ST, W, M, S, HP, HSS),
and prints formatted code lines for each section with their geometric properties.

Functionality:
- Reads the AISC shapes database from a remote Excel file.
- For WT, MT, ST sections: extracts and prints flange width (bf), flange thickness (tf), web depth (d - tf), and web thickness (tw).
- For W, M, S, HP sections: skips T-sections and MC-sections, then extracts and prints flange width (bf), flange thickness (tf), web depth (d - 2*tf), and web thickness (tw).
- For rectangular HSS sections: calculates average height (ht) and width (b), and prints these with thickness (tdes).
- For round HSS sections: extracts outside diameter (OD) and prints radius and thickness (tdes).

Note:
- The script assumes the AISC_Manual_Label and relevant geometric columns exist in the Excel file.
- Skips rows with missing or invalid geometric data.
"""

import pandas


def run():
    section_table = pandas.read_excel(
        "https://www.aisc.org/globalassets/product-files-not-searched/manuals/aisc-shapes-database-v16.0.xlsx",
        sheet_name=1,
        storage_options={"User-Agent": "Mozilla/5.0"},
        usecols="A:CF",
    )

    for _, row in section_table[
        section_table["AISC_Manual_Label"].str.startswith(("WT", "MT", "ST"))
    ].iterrows():
        designation = row["AISC_Manual_Label"]
        tf = row["tf"]
        tw = row["tw"]
        d = row["d"]
        bf = row["bf"]

        print(
            f'if(is_equal(type, "{designation}")) return {{{bf:.3f}, {tf:.3f}, {d - tf:.3f}, {tw:.3f}}};'
        )

    for _, row in section_table[
        section_table["AISC_Manual_Label"].str.startswith(("W", "M", "S", "HP"))
    ].iterrows():
        designation = row["AISC_Manual_Label"]
        if "T" in designation or "MC" in designation:
            continue

        tf = row["tf"]
        tw = row["tw"]
        d = row["d"]
        bf = row["bf"]

        print(
            f'if(is_equal(type, "{designation}")) return {{{bf:.3f}, {tf:.3f}, {bf:.3f}, {tf:.3f}, {d - 2 * tf:.3f}, {tw:.3f}}};'
        )

    for _, row in section_table[
        section_table["AISC_Manual_Label"].str.startswith("HSS")
    ].iterrows():
        designation = row["AISC_Manual_Label"]

        if row["Ht"] == "–":
            continue

        ht = (row["Ht"] + row["h"]) / 2
        b = (row["B"] + float(row["b"])) / 2
        tdes = row["tdes"]

        print(
            f'if(is_equal(type, "{designation}")) return {{{b:.3f}, {ht:.3f}, {tdes:.3f}}};'
        )

    for _, row in section_table[
        section_table["AISC_Manual_Label"].str.startswith("HSS")
    ].iterrows():
        designation = row["AISC_Manual_Label"]

        if row["OD"] == "–":
            continue

        radius = row["OD"]
        tdes = row["tdes"]

        print(
            f'if(is_equal(type, "{designation}")) return {{{radius / 2:.3f}, {tdes:.3f}}};'
        )


if __name__ == "__main__":
    run()
