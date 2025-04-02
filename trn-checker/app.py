import streamlit as st

# Simple Streamlit app for TRN input
def main():
    st.title("UAE TRN Checker (Simplified)")
    st.write("Enter a 15-digit Tax Registration Number (TRN) to verify it.")

    # Input for TRN
    trn = st.text_input("Enter TRN (15 digits)", max_chars=15)

    if st.button("Check TRN"):
        if len(trn) != 15 or not trn.isdigit():
            st.error("Please enter a valid 15-digit TRN.")
        else:
            # Placeholder response (mock validation)
            st.success(f"TRN {trn} is valid! (This is a mock response.)")

if __name__ == "__main__":
    main()
