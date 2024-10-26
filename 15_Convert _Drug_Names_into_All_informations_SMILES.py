import pubchempy as pcp
import streamlit as st
import pandas as pd


st.title("Truong Nguyen's apps for Chemical Information Retrieval")
st.write("You can upload a file with chemical names or manually enter a chemical name to retrieve information from PubChem.")


input_method = st.radio(
    "Select Input Method:",
    ("Upload a text file", "Enter a chemical name manually")
)

results = []


if input_method == "Upload a text file":
    uploaded_file = st.file_uploader("Upload a text file with chemical names:", type=["txt"])

    if uploaded_file and st.button("Process File"):
        for line in uploaded_file:
            chemical_name = line.decode("utf-8").strip()

            try:
                
                compound = pcp.get_compounds(chemical_name, 'name')[0]

                
                iupac_name = compound.iupac_name or "N/A"
                common_name = compound.synonyms[0] if compound.synonyms else "N/A"
                molecular_weight = compound.molecular_weight or "N/A"
                formula = compound.molecular_formula or "N/A"
                smiles = compound.canonical_smiles or "N/A"
                cid = compound.cid or "N/A"

                
                results.append({
                    "Compound Name": chemical_name,
                    "Common Name": common_name,
                    "SMILES": smiles,
                    "Molecular Weight": molecular_weight,
                    "Formula": formula,
                    "Compound CID": cid,
                    "IUPAC Name": iupac_name
                })

            except (IndexError, AttributeError):
                st.warning(f"No information found for: {chemical_name}")
                results.append({
                    "Compound Name": chemical_name,
                    "Common Name": "N/A",
                    "SMILES": "N/A",
                    "Molecular Weight": "N/A",
                    "Formula": "N/A",
                    "Compound CID": "N/A",
                    "IUPAC Name": "N/A"
                })


if input_method == "Enter a chemical name manually":
    chemical_name = st.text_input("Enter a chemical name:")

    if chemical_name and st.button("Retrieve Data"):
        try:
            
            compound = pcp.get_compounds(chemical_name, 'name')[0]

            
            iupac_name = compound.iupac_name or "N/A"
            common_name = compound.synonyms[0] if compound.synonyms else "N/A"
            molecular_weight = compound.molecular_weight or "N/A"
            formula = compound.molecular_formula or "N/A"
            smiles = compound.canonical_smiles or "N/A"
            cid = compound.cid or "N/A"

            
            results.append({
                "Compound Name": chemical_name,
                "Common Name": common_name,
                "SMILES": smiles,
                "Molecular Weight": molecular_weight,
                "Formula": formula,
                "Compound CID": cid,
                "IUPAC Name": iupac_name
            })

        except (IndexError, AttributeError):
            st.warning(f"No information found for: {chemical_name}")
            results.append({
                "Compound Name": chemical_name,
                "Common Name": "N/A",
                "SMILES": "N/A",
                "Molecular Weight": "N/A",
                "Formula": "N/A",
                "Compound CID": "N/A",
                "IUPAC Name": "N/A"
            })


if results:
    
    df = pd.DataFrame(results)

    
    st.write("### Chemical Information Table")
    st.dataframe(df)

    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="Your_Converted_Chemical_info.csv",
        mime="text/csv"
    )
