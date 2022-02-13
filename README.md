# Read NDEF using PC/SC reader

**Compatible tags:** NTAG® 213, NTAG® 215, NTAG® 216.

**Compatible readers:** Identiv uTrust 3700F, 3720F. Other similiar readers from Identiv/SCM Microsystems might also work.

*Note:* NTAG - is a trademark of NXP B.V. uTrust - is a trademark of Identiv Inc. This project is not affiliated with NXP nor Identiv.

## Usage

```
pip3 install -r requirements.txt
python3 read_tag.py
```

**Example output:**

```
Alcor Micro USB Smart Card Reader 0 no card inserted
Identiv uTrust 3720 Contactless Reader 0 3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 00 03 00 00 00 00 68
[ndef.uri.UriRecord('https://nfcdeveloper.com')]
```

## Contact us

Trying to build an NFC solution? Not sure how to do it? We could help you with that! Please fill out our [inquiry form](https://nfcdeveloper.com/contact/) or drop a short email to [mike@nfcdeveloper.com](mailto:mike@nfcdeveloper.com).
