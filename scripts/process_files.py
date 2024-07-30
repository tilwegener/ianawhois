import os
import re

def parse_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
    
    def get_value(pattern):
        match = re.search(pattern, content)
        return match.group(1).replace('\n', ' ') if match else None
    
    data = {
        'domain': get_value(r'domain:\s*(\S+)'),
        'organisation': get_value(r'organisation:\s*(.*)'),
        'address': get_value(r'address:\s*(.*(?:\naddress:.*)*)'),
        'contact_administrative_name': get_value(r'contact:\s+administrative\s+name:\s*(.*)'),
        'contact_administrative_organisation': get_value(r'contact:\s+administrative\s+organisation:\s*(.*)'),
        'contact_administrative_address': get_value(r'contact:\s+administrative\s+address:\s*(.*(?:\naddress:.*)*)'),
        'contact_administrative_phone': get_value(r'contact:\s+administrative\s+phone:\s*(.*)'),
        'contact_administrative_fax_no': get_value(r'contact:\s+administrative\s+fax-no:\s*(.*)'),
        'contact_administrative_email': get_value(r'contact:\s+administrative\s+e-mail:\s*(.*)'),
        'contact_technical_name': get_value(r'contact:\s+technical\s+name:\s*(.*)'),
        'contact_technical_organisation': get_value(r'contact:\s+technical\s+organisation:\s*(.*)'),
        'contact_technical_address': get_value(r'contact:\s+technical\s+address:\s*(.*(?:\naddress:.*)*)'),
        'contact_technical_phone': get_value(r'contact:\s+technical\s+phone:\s*(.*)'),
        'contact_technical_fax_no': get_value(r'contact:\s+technical\s+fax-no:\s*(.*)'),
        'contact_technical_email': get_value(r'contact:\s+technical\s+e-mail:\s*(.*)'),
        'nserver': get_value(r'nserver:\s*(.*(?:\n.*)*)'),
        'ds_rdata': get_value(r'ds-rdata:\s*(.*)'),
        'whois': get_value(r'whois:\s*(.*)'),
        'status': get_value(r'status:\s*(.*)'),
        'remarks': get_value(r'remarks:\s*(.*)'),
        'created': get_value(r'created:\s*(\d{4}-\d{2}-\d{2})'),
        'changed': get_value(r'changed:\s*(\d{4}-\d{2}-\d{2})'),
        'source': get_value(r'source:\s*(.*)'),
    }
    
    return data

def generate_sql(data):
    sql = "INSERT INTO domain_info (domain, organisation, address, contact_administrative_name, contact_administrative_organisation, contact_administrative_address, contact_administrative_phone, contact_administrative_fax_no, contact_administrative_email, contact_technical_name, contact_technical_organisation, contact_technical_address, contact_technical_phone, contact_technical_fax_no, contact_technical_email, nserver, ds_rdata, whois, status, remarks, created, changed, source) VALUES ("
    sql += ", ".join(f"'{str(value).replace('\'', '\'\'')}'" if value else "NULL" for value in data.values())
    sql += ");\n"
    return sql

def main():
    directory = '.'
    output_sql_file = 'output.sql'
    
    with open(output_sql_file, 'w') as sql_file:
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                filepath = os.path.join(directory, filename)
                data = parse_file(filepath)
                sql_file.write(generate_sql(data))

if __name__ == "__main__":
    main()
