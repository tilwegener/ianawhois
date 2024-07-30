import os
import re
import sqlite3

def escape_sql(value):
    """Escapes single quotes and other problematic characters in SQL strings."""
    if value is None:
        return 'NULL'
    value = value.replace("'", "''")  # Escape single quotes
    return f"'{value}'"

def parse_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

    def extract_field(label, content):
        match = re.search(f'{label}:\s*(.*?)(?=\n\S+:|$)', content, re.DOTALL)
        return match.group(1).strip() if match else None

    def extract_multi_field(label, content):
        matches = re.findall(f'{label}:\s*(.*?)(?=\n\S+:|$)', content, re.DOTALL)
        return ', '.join(m.strip() for m in matches) if matches else None

    return {
        'domain': os.path.basename(filepath),
        'organisation': extract_field('organisation', content),
        'address': extract_multi_field('address', content),
        'contact_administrative_name': extract_field('name', content),
        'contact_administrative_organisation': extract_field('organisation', content),
        'contact_administrative_address': extract_multi_field('address', content),
        'contact_administrative_phone': extract_field('phone', content),
        'contact_administrative_fax_no': extract_field('fax-no', content),
        'contact_administrative_email': extract_field('e-mail', content),
        'contact_technical_name': extract_field('name', content),
        'contact_technical_organisation': extract_field('organisation', content),
        'contact_technical_address': extract_multi_field('address', content),
        'contact_technical_phone': extract_field('phone', content),
        'contact_technical_fax_no': extract_field('fax-no', content),
        'contact_technical_email': extract_field('e-mail', content),
        'nserver': extract_multi_field('nserver', content),
        'ds_rdata': extract_field('ds-rdata', content),
        'whois': extract_field('whois', content),
        'status': extract_field('status', content),
        'remarks': extract_field('remarks', content),
        'created': extract_field('created', content),
        'changed': extract_field('changed', content),
        'source': extract_field('source', content),
    }

def generate_sql(data):
    sql = f"""
    INSERT INTO domain_tld_whois (
        domain, organisation, address, contact_administrative_name, contact_administrative_organisation, contact_administrative_address, contact_administrative_phone, contact_administrative_fax_no, contact_administrative_email,
        contact_technical_name, contact_technical_organisation, contact_technical_address, contact_technical_phone, contact_technical_fax_no, contact_technical_email, nserver, ds_rdata, whois, status, remarks, created, changed, source
    ) VALUES (
        {escape_sql(data['domain'])}, {escape_sql(data['organisation'])}, {escape_sql(data['address'])}, {escape_sql(data['contact_administrative_name'])}, {escape_sql(data['contact_administrative_organisation'])}, {escape_sql(data['contact_administrative_address'])}, {escape_sql(data['contact_administrative_phone'])}, {escape_sql(data['contact_administrative_fax_no'])}, {escape_sql(data['contact_administrative_email'])},
        {escape_sql(data['contact_technical_name'])}, {escape_sql(data['contact_technical_organisation'])}, {escape_sql(data['contact_technical_address'])}, {escape_sql(data['contact_technical_phone'])}, {escape_sql(data['contact_technical_fax_no'])}, {escape_sql(data['contact_technical_email'])}, {escape_sql(data['nserver'])}, {escape_sql(data['ds_rdata'])}, {escape_sql(data['whois'])}, {escape_sql(data['status'])}, {escape_sql(data['remarks'])}, {escape_sql(data['created'])}, {escape_sql(data['changed'])}, {escape_sql(data['source'])}
    );
    """
    return sql

def main():
    directory = '.'  # Root-Verzeichnis
    output_sql_file = 'output.sql'
    
    with open(output_sql_file, 'w') as sql_file:
        for filename in os.listdir(directory):
            if filename:  # Überprüfe, ob es sich um eine .txt-Datei handelt
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):  # Stelle sicher, dass es sich um eine Datei handelt
                    data = parse_file(filepath)
                    sql_content = generate_sql(data)
                    sql_file.write(sql_content + '\n')

if __name__ == "__main__":
    main()
