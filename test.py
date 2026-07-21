# # 

# uv run python -c "

# from app.security import PIIDetector
# detector=PIIDetector()
# text='''

# Please help John at john.doe@example.com
# or  call 555-123-4567
# his SSN is 123-45-6789
# and card number is 4111-1111-1111-1111

# '''
# print('==================ORIGINAL=================')
# print(text)

# print('====================== Detected PII=====')
# found= detector.detect(text)
# for pii_type,values in found.items():
#     print(f"\n{pii_type.upper()}:{values}")
   
# print()
# print(f'=============Masked=====================')
# masked=detector.mask(text)
# print(masked) "
