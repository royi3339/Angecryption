
a angecryption program, that decrypt / encrypt pdf/png file inside other pdf/png  file.

this verion is the regular angecryption:
(in the hide-file1-file2 its decrypt file1, then concat file2 to it, and then encrypt it all - [file1 returns to be a readable file...] ).
(in the "decrypt-to-file" its decrypt the full file, and then make a swap between the files...).

warning!: if we enter a wrong iv in the action of "decrypt-to-file" the result will be perfect!.
	this is because we swap the order of the files, and the wrong iv influenced only on the first block of the file!

solution - we can use the second option "reversed angecryption" - that making the enc/dec opposite to the dec/enc actions. 

this "regular angecryption" should be great, because the iv is not a secret in anyway...

i didnt validated the "POC" of the "reversed angecryption" version, just changed the order of the enc/dec which should be the same influenced of a cryptography point of view...



requires:
need to download: pycryptodome library.
