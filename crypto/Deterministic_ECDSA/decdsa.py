from fastecdsa.curve import Curve
from hashlib import sha256, sha512
from Crypto.Util.number import inverse as modinv
from base64 import b64encode as b64e, b64decode as b64d

def sign(C, sk, msg):
	ctx = sha256()
	ctx.update(msg.encode())
	k = int(ctx.hexdigest(), 16)

	ctx = sha512()
	ctx.update(msg.encode())
	h = int(ctx.hexdigest(), 16)

	P = k * C.G
	r = P.x
	assert r > 0, "Error: cannot sign this message."

	s = (modinv(k, C.q) * (h + sk * r)) % C.q
	assert s > 0, "Error: cannot sign this message."

	return (r, s)

def verify(C, Q, msg, r, s):

	if Q.IDENTITY_ELEMENT == Q:
		return False

	if not C.is_point_on_curve((Q.x, Q.y)):
		return False

	if r < 1 or r > C.q - 1:
		return False

	if s < 1 or s > C.q - 1:
		return False

	ctx = sha512()
	ctx.update(msg.encode())
	h = int(ctx.hexdigest(), 16)

	s_inv = modinv(s, C.q)
	u = h * s_inv % C.q
	v = r * s_inv % C.q
	P = u * C.G + v * Q
	return r == P.x

if __name__ == "__main__":

	sk = int(open("sk.txt", "r").read())

	C = Curve(
	    "ANSSIFRP256v1",
	    0xF1FD178C0B3AD58F10126DE8CE42435B3961ADBCABC8CA6DE8FCF353D86E9C03,
	    0xF1FD178C0B3AD58F10126DE8CE42435B3961ADBCABC8CA6DE8FCF353D86E9C00,
	    0xEE353FCA5428A9300D4ABA754A44C00FDFEC0C9AE4B1A1803075ED967B7BB73F,
	    0xF1FD178C0B3AD58F10126DE8CE42435B53DC67E140D2BF941FFDD459C6D655E1,
	    0xB6B3D4C356C139EB31183D4749D423958C27D2DCAF98B70164C97A2DD98F5CFF,
	    0x6142E0F7C8B204911F9271F0F3ECEF8C2701C307E8E4C9E183115A1554062CFB
	)

	print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
	print("=-= ECC-Based Secure Flag Storage =-=")
	print("=-=      (under development)      =-=")
	print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

	Q = sk * C.G
	print("Public Point Q:")
	print("  Q.x: 0x{:064x}".format(Q.x))
	print("  Q.y: 0x{:064x}".format(Q.y))

	print("What is your name?")
	while True:
		username = input(">>> ")
		if "|" not in username: break

	print("Here are a few user tokens:")
	for i in range(4):
		uid = "{}_#{:02x}".format(username, i)
		r, s = sign(C, sk, uid)
		token = b64e("{}|{}|{}".format(uid, r, s).encode()).decode()
		print(token)

	print("Access to flag is limited to admin user.")
	print("Enter admin token:")
	token = input(">>> ")
	token = b64d(token.encode()).decode().split('|')
	if token[0] != "admin":
		print("Error: access forbidden")
		exit(1)

	r, s = map(int, token[1:])
	if verify(C, Q, "admin", r, s):
		flag = open("flag.txt", "r").read()
		print("Here is the stored flag: {}".format(flag))
	else:
		print("Error: access forbidden")

