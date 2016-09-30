#subst alfabet. 0 = A, 26 = Z, foo(i) gjør om bokstaven.

#caesar-sipher. index i -> i + m mod N, m er nøkkelen (1, 2, ..., k)
#UWEEGUU -> SUCCESS
#ved å kryptere UWEEGUU med nøkkel n = 24 (26-key) får vi teksten tilbake

#multiplikasjons-cipher. bytter bokstav med verdi "i": i -> i*m mod N, eks B med nøkkel 3: 1->1*3 mod 26. 26 er størrelsen på tabellen.
# må finnes en n: m * n mod N = 1. bruker modular_inverse

#affine: i -> i*m1 + m2:
# først caesar med nøkkel n2, matcher m2
# så multiplikasjon med nkkel n1 som matcher m1
#m er en tuppel (m1, m2), samme for (n1, n2)

#RSA
#mottaker oppgir nøkkel, umulig å knekke.
'''
How to: nøkler:
to random primtall: P og Q
n = P*Q
theta = (P-1)*(Q-1)
e, hvor 2 < e < theta

til sist: D: D*e mod (theta) = 1 
bruk modular_inverse

fra dette blir (n, e) den OFFENTLIGE nøkkelen
(n, d) er den hemmelige nøkkelen for dekryptering

kryptering:
c = (t^e) mod n, c = pow(t, e, n)
dekryptering:
t' = (c^d) mod n, hvor t' = t

algoritme:

tar inn positive heltall og krypterer.

del opp i blokker
for hver blokk:
	for hver symbol i blokk:
		finn ASCII verdi i binærformat
		slå sammen binærstrenger og finn desimalverdi

deretter får vi en streng av sammenslåtte heltallverdier

(blocks_from_text og text_from_blocks)
'''

#hacker. må vurdere dekrypteringsnøkkel fra "plain-text" gitt en krypteringsalgoritme. Sammenligner ordene med en liste (english_owrds.txt)
#null match: ferdig. fortsetter til beste resultat.
#skal knekke alle bortsett fra RSA


'''
OTHER NOTES:
En superklasse med verdier som alle sub-cipherne skal arve fra
*CIPHER:
	- Nøkkel-par (n,m) slik at n+m mod 26 = 0
		- Lag en counter-nøkkel for hver (objekt?)
	- Broadcaste mulige nøkler for hackeren
	
*Personer:
	- Sender, Mottaker, Hacker
		- Jobber mot et cipher
		- Har en tekst de vil oversette fra cipher<->tekst
		- har en nøkkel/sett med nøkler
	Subklasser!
'''
import binascii

def chars_to_ascii(str):
	print(str + " as ascii...")
	for c in str:
		print(ord(c), end = ' ')
	print()
	
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def to_binary(str):
	return (bin(int.from_bytes(str.encode(), 'big')))

def test():
	_s = "dette skal dekodes".upper()
	chars_to_ascii(_s)
	
test()