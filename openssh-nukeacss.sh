#!/bin/sh
#
#  Remove the ACSS implementation from OpenSSH, and disable its use so that the
#  rest of the package can still be built.
#
> acss.c
patch -sp1 << EOF
--- openssh/cipher.c
+++ openssh/cipher.c
@@ -53,6 +53,7 @@
 extern void ssh_rijndael_iv(EVP_CIPHER_CTX *, int, u_char *, u_int);
 #endif
 
+#if 0
 #if !defined(EVP_CTRL_SET_ACSS_MODE)
 # if (OPENSSL_VERSION_NUMBER >= 0x00907000L)
 extern const EVP_CIPHER *evp_acss(void);
@@ -62,6 +63,9 @@
 #  define EVP_acss NULL /* Don't try to support ACSS on older OpenSSL */
 # endif /* (OPENSSL_VERSION_NUMBER >= 0x00906000L) */
 #endif /* !defined(EVP_CTRL_SET_ACSS_MODE) */
+#else
+#define EVP_acss NULL
+#endif /* 0 */
 
 extern const EVP_CIPHER *evp_ssh1_bf(void);
 extern const EVP_CIPHER *evp_ssh1_3des(void);
EOF
