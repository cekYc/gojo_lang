import sys
import os
import re

# --- GLOBAL HAFIZA ---
memory = {}

# --- İFADE TEMİZLEYİCİ ---
def clean_expr(expr):
    if not isinstance(expr, str): return expr
    
    placeholders = {}
    def mask_string(match):
        key = f"___STR{len(placeholders)}___"
        placeholders[key] = match.group(0)
        return key
    masked_expr = re.sub(r'("[^"]*")', mask_string, expr)

    # --- MANTIK DÖNÜŞÜMLERİ ---
    
    # 1. Mevcut '!=' işaretlerini korumaya al
    masked_expr = masked_expr.replace('!=', '___NEQ___')

    # 2. SENİN ÖNERİN: 'isnt' -> '!=' (Placeholder'a çeviriyoruz)
    # Boşluklu ' isnt ' arıyoruz ki değişken isimleriyle karışmasın
    masked_expr = masked_expr.replace(' isnt ', ' ___NEQ___ ')
    
    # Geriye dönük uyumluluk için 'is not'ı da destekleyebiliriz ama
    # senin isteğin üzerine sadeleştiriyoruz.

    # 3. Diğer Operatörler
    masked_expr = masked_expr.replace('&&', ' and ')
    masked_expr = masked_expr.replace('||', ' or ')
    masked_expr = masked_expr.replace('!', ' not ') 
    
    # 4. Korumaları Kaldır
    masked_expr = masked_expr.replace('___NEQ___', '!=')
    
    for key, val in placeholders.items(): masked_expr = masked_expr.replace(key, val)
    
    return masked_expr

# --- TİP KONTROL ---
def parse_value(hedef_tip, ifade):
    temiz_ifade = clean_expr(ifade)
    try: deger = eval(temiz_ifade, {}, memory)
    except: deger = ifade

    if '[]' in hedef_tip:
        if not isinstance(deger, list): raise ValueError(f"Dizi hatasi: '{deger}'")
        ana_tip = hedef_tip.replace('[]', '') 
        yeni_liste = []
        for item in deger: yeni_liste.append(parse_value(ana_tip, str(item)))
        return yeni_liste

    if hedef_tip == 'int':
        try: return int(deger)
        except: raise ValueError(f"Int hatasi: '{deger}'")
    elif hedef_tip == 'double':
        try: return float(deger)
        except: raise ValueError(f"Double hatasi: '{deger}'")
    elif hedef_tip == 'string':
        try: return str(deger)
        except: raise ValueError(f"String hatasi: '{deger}'")
    elif hedef_tip == 'bool':
        val = str(deger).lower()
        if val not in ['true', 'false']: raise ValueError(f"Bool hatasi: '{deger}'")
        return val == 'true'
    elif hedef_tip == 'char':
        text = str(deger)
        if len(text) > 1 or len(text) == 0: raise ValueError(f"Char hatasi: '{text}'")
        return text
    return deger

# --- FORMATLAMA ---
def format_text(text):
    if not isinstance(text, str): return text
    bulunan = re.findall(r'\{([^}]+)\}', text)
    for ifade in bulunan:
        try:
            val = eval(clean_expr(ifade), {}, memory)
            text = text.replace("{" + ifade + "}", str(val))
        except Exception as e: raise ValueError(f"Metin ici ifade hatasi: '{{{ifade}}}' -> {e}")
    text = text.replace(r'\n', '\n').replace(r'\t', '\t').replace(r'\"', '"')
    return text

def run_gojo_v6(filename):
    if not os.path.exists(filename):
        print(f"❌ HATA: '{filename}' bulunamadı.")
        return

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    print(f"🚀 Gojo v6.0 (Isnt Update) Çalışıyor: {filename}\n")
    print("-" * 30)
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # String dışındaki yorumları temizle
        in_string = False
        comment_pos = -1
        for idx, ch in enumerate(line):
            if ch == '"' and (idx == 0 or line[idx-1] != '\\'):
                in_string = not in_string
            elif ch == '#' and not in_string:
                comment_pos = idx
                break
        if comment_pos != -1:
            line = line[:comment_pos].strip()
        if not line:
            i += 1
            continue

        first_word = line.split()[0]

        # --- 1. TANIMLAMA ---
        if first_word in ['int', 'string', 'double', 'bool', 'char']:
            if ',' in line and '=' not in line: 
                vars_part = line[len(first_word):].strip()
                var_list = [v.strip() for v in vars_part.split(',')]
                for var_name in var_list:
                    if first_word == 'int': memory[var_name] = 0
                    elif first_word == 'string': memory[var_name] = ""
                    elif first_word == 'double': memory[var_name] = 0.0
                    elif first_word == 'bool': memory[var_name] = False
            elif '=' in line:
                parts = line.split('=', 1)
                sol = parts[0].strip().split()
                sag = parts[1].strip()
                tip, isim = sol[0], sol[1]
                try:
                    if sag.startswith('input'):
                        soru = sag[5:].strip().strip('"') if len(sag) > 5 else ""
                        val = input(soru + " ")
                        memory[isim] = parse_value(tip, f'"{val}"')
                    else:
                        memory[isim] = parse_value(tip, sag)
                except Exception as e:
                    print(f"❌ HATA (Satır {i+1}): {e}")
                    return
            else:
                parts = line.split()
                if len(parts) > 1:
                    var = parts[1]
                    if first_word == 'int': memory[var] = 0
                    elif first_word == 'string': memory[var] = ""
                    elif first_word == 'double': memory[var] = 0.0
                    elif first_word == 'bool': memory[var] = False
                    elif first_word == 'char': memory[var] = ''

        # --- 2. GÜNCELLEME ---
        elif '=' in line and first_word not in ['if', 'while', 'for', 'print', 'println', 'con']:
            parts = line.split('=', 1)
            var_expr, expr = parts[0].strip(), parts[1].strip()
            try:
                if '[' in var_expr and ']' in var_expr: 
                    base_name = var_expr.split('[')[0]
                    if base_name in memory:
                        val = eval(clean_expr(expr), {}, memory)
                        mevcut = eval(var_expr, {}, memory)
                        if isinstance(mevcut, int) and not isinstance(mevcut, bool): val = int(val)
                        elif isinstance(mevcut, float): val = float(val)
                        exec(f"memory['{base_name}']{var_expr[len(base_name):]} = {val}")
                    else: print(f"HATA: '{base_name}' yok.")
                elif var_expr in memory:
                    eski = memory[var_expr]
                    if expr.startswith('input'):
                        soru = expr[5:].strip().strip('"') if len(expr) > 5 else ""
                        val = input(soru + " ")
                    else:
                        val = eval(clean_expr(expr), {}, memory)

                    if isinstance(eski, bool): val = str(val).lower() == 'true'
                    elif isinstance(eski, int): val = int(val)
                    elif isinstance(eski, float): val = float(val)
                    elif isinstance(eski, str): val = str(val)
                    memory[var_expr] = val
                else: print(f"HATA: '{var_expr}' tanımlı değil.")
            except Exception as e: print(f"Atama hatasi: {e}")

        # --- 3. PRINT / PRINTLN ---
        elif first_word == 'print':
            expr = line[5:].strip()
            try:
                res = eval(clean_expr(expr), {}, memory)
                print(f"{format_text(str(res))}", end='', flush=True)
            except Exception as e: print(f"HATA: {e}")

        elif first_word == 'println':
            if len(line.strip()) == 7: print()
            else:
                expr = line[7:].strip()
                try:
                    res = eval(clean_expr(expr), {}, memory)
                    print(f"{format_text(str(res))}")
                except Exception as e: print(f"HATA: {e}")

        # --- 4. FOR ---
        elif first_word == 'for':
            try:
                match = re.search(r'for\s+(\w+)\s*=\s*(.+?)\s+to\s+(.+?)(?:\s+but\s+(.+))?$', line)
                if match:
                    var_name = match.group(1)
                    try:
                        start_val = int(eval(match.group(2), {}, memory))
                        end_val = int(eval(match.group(3), {}, memory))
                        step_val = 1
                        if match.group(4): step_val = int(eval(match.group(4), {}, memory))
                    except: return
                    memory[var_name] = start_val
                    skip_loop = False
                    if step_val > 0 and start_val > end_val: skip_loop = True
                    elif step_val < 0 and start_val < end_val: skip_loop = True
                    if skip_loop:
                        nested = 0
                        while i < len(lines):
                            i += 1
                            if i >= len(lines): break
                            curr = lines[i].strip().split()[0]
                            if curr == 'for': nested += 1
                            elif curr == 'con':
                                if nested == 0: break
                                nested -= 1
            except: pass

        # --- 5. CON ---
        elif first_word == 'con':
            nested = 0
            temp_i = i - 1
            found_for = False
            while temp_i >= 0:
                s_line = lines[temp_i].strip()
                if not s_line:
                    temp_i -= 1
                    continue
                s_word = s_line.split()[0]
                if s_word == 'con': nested += 1
                elif s_word == 'for':
                    if nested == 0:
                        match = re.search(r'for\s+(\w+)\s*=\s*(.+?)\s+to\s+(.+?)(?:\s+but\s+(.+))?$', s_line)
                        if match:
                            var_name = match.group(1)
                            end_val = int(eval(match.group(3), {}, memory))
                            step_val = 1
                            if match.group(4): step_val = int(eval(match.group(4), {}, memory))
                            memory[var_name] += step_val
                            current_val = memory[var_name]
                            should_continue = False
                            if step_val > 0 and current_val <= end_val: should_continue = True
                            elif step_val < 0 and current_val >= end_val: should_continue = True
                            if should_continue: i = temp_i
                            found_for = True
                            break
                    else: nested -= 1
                temp_i -= 1

        # --- 6. IF ---
        elif first_word == 'if':
             expr = line[2:].strip()
             try:
                # clean_expr 'isnt' -> '!=' yapacak
                condition = eval(clean_expr(expr), {}, memory)
                
                if not condition:
                    nested = 0
                    while i < len(lines):
                        i += 1
                        if i >= len(lines): break
                        curr = lines[i].strip().split()[0]
                        if curr == 'if': nested += 1
                        elif curr == 'finn':
                            if nested == 0: break
                            nested -= 1
                        elif curr == 'else':
                            if nested == 0: break
             except Exception as e:
                 print(f"❌ IF HATASI (Satır {i+1}): {e}")
                 return

        # --- 7. ELSE ---
        elif first_word == 'else':
             nested = 0
             while i < len(lines):
                i += 1
                if i >= len(lines): break
                curr = lines[i].strip().split()[0]
                if curr == 'if': nested += 1
                elif curr == 'finn':
                    if nested == 0: break
                    nested -= 1

        # --- 8. WHILE ---
        elif first_word == 'while':
             expr = line[5:].strip()
             try:
                 if not eval(clean_expr(expr), {}, memory):
                     nested = 0
                     while i < len(lines):
                         i += 1
                         if i >= len(lines): break
                         curr = lines[i].strip().split()[0]
                         if curr == 'while': nested += 1
                         elif curr == 'end':
                             if nested == 0: break
                             nested -= 1
             except Exception as e:
                 print(f"❌ WHILE HATASI (Satır {i+1}): {e}")
                 return

        elif first_word == 'finn': pass
        elif first_word == 'end':
            temp_i = i - 1
            while temp_i >= 0:
                s = lines[temp_i].strip()
                if not s: 
                    temp_i -= 1
                    continue
                if s.startswith('while') and 'end' not in lines[temp_i:i]:
                    if eval(clean_expr(s[5:].strip()), {}, memory): i = temp_i
                    break
                temp_i -= 1

        i += 1
    print("\n" + "-" * 30)

if __name__ == "__main__":
    if len(sys.argv) > 1: run_gojo_v6(sys.argv[1])
    else: print("Dosya adı girin.")