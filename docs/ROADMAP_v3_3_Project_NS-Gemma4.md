# ROADMAP v3.3: Project NS-Gemma4 (selaras MASTER PRD v3.4 §11)

Rabu, 18 Nov 2026 · menggantikan ROADMAP v3.2 · tambahan: version control & backup GitHub

**Catatan asal [A]:** ROADMAP v3.2 tidak tersedia saat dokumen ini disusun. Isi jadwal, gerbang, dan skenario F4 di bawah **disalin dari MASTER PRD v3.4 §11**, lalu ditambah langkah GitHub. Bila ROADMAP v3.2 asli memuat butir yang tidak ada di PRD v3.4, lakukan `diff` manual sebelum menimpa berkasnya; butir itu berstatus [K] sampai dicocokkan.

**Legenda (sama dengan PRD):** [V\*] dokumen resmi per kutipan ROLE.md, belum dicocokkan ke berkas asli sampai V-01 lulus · [K] laporan komunitas/dokumen turunan · [A] asumsi rekayasa tim · [U] laporan pengguna tentang lingkungannya, belum diperiksa.

---

## 1. Ringkasan perubahan terhadap PRD §11

| # | Perubahan | Alasan |
| --- | --- | --- |
| 1 | F0 mendapat sub-langkah **F0.0** (pengaman repositori & backup, target ≤30 menit) sebelum inspeksi V-test | Dokumen arsitektur terlindungi dari salah hapus sebelum fase iterasi cepat |
| 2 | Cek **GH-1..GH-6** (§5) menjadi syarat *push*, **bukan** syarat G0/S1 | Batas G0 (Kam 19 Nov 06:59 WIB) tidak boleh tertahan urusan repo |
| 3 | Checkpoint commit di tiap gerbang G0–G4 dan **tag per submission** memuat hash zip | Memenuhi pencatatan "hash zip, konfigurasi, hasil" di PRD §10.4 |
| 4 | `.gitignore` diperketat (kredensial, `*.jsonl`, folder aset kompetisi, `.env`) | Mencegah pelanggaran data/kredensial (PRD §1 "Lisensi/data") |
| 5 | F4 pembekuan = tag `freeze-*`; F5 hanya hotfix ber-commit | Jejak reproduksibilitas pada kandidat final |
| 6 | Register risiko +4 baris (§8) dan usulan sinkronisasi PRD (§9) | Konsistensi dokumen |

**Tidak berubah:** semua tanggal, gerbang G1–G5 (selain catatan checkpoint), Skenario A/B, angka 81 jam [K], daftar V-test.

---

## 2. Fakta yang mendasari tambahan GitHub

| Item | Status |
| :-- | :-- |
| Repositori `005-rgb/Project-JOBEN-Gemma4` ada dan dikelola pengguna | [U] |
| Visibilitas repositori saat ini `Private` | [U], **belum diperiksa** → GH-1 |
| Berbagi kode privat di luar tim = diskualifikasi; data kompetisi tidak boleh dibagikan | [V\*] (PRD §1 "Lisensi/data"); cakupan V-01 diperluas: cocokkan bunyi Rules, termasuk apakah repo privat dengan kolaborator di luar tim dihitung berbagi |
| Pemenang wajib merilis di bawah lisensi OSI (Apache 2.0) | [V\*] |
| Direktori kerja `/home/vboxuser/gemma4-agent/` memuat `docs/`, `data/`, `.venv/`; `.gitignore` sudah ada; kredensial di `/home/vboxuser/.kaggle/` | [U] |
| Nama repo "JOBEN" berbeda dari nama proyek di PRD ("NS-Gemma4") | Hanya penamaan; tidak memengaruhi kepatuhan. Cantumkan alias di `README` repo bila perlu |

---

## 3. Jadwal & gerbang (WIB)

Hari ini Rabu 18 Nov 2026; batas hari kiriman diasumsikan UTC [K] (V-31).

| Fase & rentang | Fokus | Gerbang |
| :-- | :-- | :-- |
| **F0** 18 Nov | **F0.0 (+GH)** pengaman repositori & push dokumen (§5) → inspeksi baca-saja `HARNESS_README.md`, `sample_submission`, `tasks.jsonl` (V-01, V-06, V-07, V-10, V-12) dan status [U] → susun & validasi Varian 0 → kirim **S1** (`max_time_minutes: 4`) | **G0:** compiler resmi lulus dan S1 antre sebelum Kam 19 Nov 06:59 WIB. **(+GH)** push dokumen dikerjakan lebih dulu tetapi bukan syarat G0; bila satu cek GH gagal, jangan push dan lanjutkan F0 |
| **F1** 18–20 Nov | Gold-check M11 (M ≥ 30 + 10 hold-out); benchmark §2.3; run dev lebar + bootstrap M15; **S2** (Varian 0 + `L`); V-31 diuji dengan perilaku antrean S1/S2. **(+GH)** commit `submission_root/` Varian 0 + `experiments/LOG.md`; tag `s1-…`, `s2-…` | **G1:** waktu antrean nyata terukur, `L` terkunci, keputusan 12B |
| **F2** 19–22 Nov | V-15..V-17, V-25..V-30; tulis & unit-test `funnel.py`; diagnosis M12 pada E4B (P=6). **(+GH)** commit `skills/funnel/`, `sub_agents/`, `prompts/`, skrip build (`tools/`), unit test | **G2 (GO/NO-GO):** §2.4 PRD. Commit hasil gerbang (lulus atau buang) dengan pesan yang memuat keputusan |
| **F3** 23–25 Nov | Saringan R=1 lalu konfirmasi R=3; **S3**; verifikasi ulang status `Joined` sebelum 26 Nov 06:59 WIB. **(+GH)** commit ringkasan agregat hasil (tanpa teks tugas); tag `s3-…` | **G3:** pemenang memenuhi Tier-C/Tier-S |
| **F4** pembekuan | Skenario A/B (§4). **(+GH)** tag `freeze-final-a` / `freeze-final-b` pada commit yang dikirim; `git push origin --tags` | **G4:** kandidat final masuk antrean sesuai skenario; hash zip di `LOG.md` = hash zip yang dikirim |
| **F5** 30 Nov–2 Des | Pantau antrean (hanya hotfix format bila ditolak); pilih tepat 2 submission final di Kaggle sebelum **Kam 3 Des 06:59 WIB**. **(+GH)** tiap hotfix = 1 commit + 1 tag baru | **G5:** 14 kriteria §14 PRD terpenuhi |

### 3.1 Urutan F0 (rinci)

1. **F0.0** GH-1 → GH-6 (§5). Batas waktu ≈30 menit; lewat batas, hentikan dan lanjut ke langkah 2 (repo dikerjakan ulang setelah S1 antre).
2. Inspeksi baca-saja `data/` (hanya `cat`/`head`/`jq`; tidak menulis ke `data/`): V-01, V-06, V-07, V-10, V-12 dan status [U] (akun `Joined`, aset di `/home/vboxuser/...`, `.venv/`).
3. Setelah inspeksi: `git status --short` harus tetap tidak menampilkan `data/` maupun `.venv/` (tidak terlacak, tidak berubah staging).
4. Susun & validasi Varian 0 dengan compiler resmi + `package_and_validate.py`.
5. Kirim S1; catat hash zip di `experiments/LOG.md`; commit + tag `s1-…`; push.

---

## 4. Skenario F4 (diputuskan oleh V-31; turunan angka 81 jam [K])

- **Skenario A (≥2 submission boleh pending):** bekukan kode Kam 26 Nov; kirim S4 (Final A) dan S5 (Final B) pada hari berbeda (1/hari [K]); **S5 paling lambat Min 29 Nov 18:00 WIB**: 18:00 + 81 jam = Kam 3 Des 03:00 WIB < 06:59 WIB.
- **Skenario B (1 pending, serial):** dua kiriman final baru tidak muat. Batas kirim S4 = 29 Nov 18:00 − 81 jam = **Kam 26 Nov 09:00 WIB**, sehingga kode Final A dibekukan **Rabu 25 Nov**. **Final B diambil dari submission yang sudah bernilai** (mis. S3 bila E4B); hanya satu kiriman final baru.
- Pada kedua skenario, 2 final dipilih dari submission yang sudah selesai dinilai; submission tertahan antrean bukan kandidat final yang aman.
- **(+GH)** Tag `freeze-*` dibuat pada commit yang menghasilkan zip yang dikirim, bukan sesudahnya.

---

## 5. Prosedur GitHub (F0.0)

Aturan keras: **bila satu cek gagal, jangan `git push`.**

### GH-1. Pastikan repositori `Private` SEBELUM push
- Buka `https://github.com/005-rgb/Project-JOBEN-Gemma4` di jendela *incognito* tanpa login: harus menampilkan 404. [A]
- Di GitHub: *Settings → General → Danger Zone* menunjukkan visibilitas `Private`; *Settings → Collaborators* hanya berisi anggota tim.
- Opsional bila `gh` terpasang: `gh repo view 005-rgb/Project-JOBEN-Gemma4 --json visibility`.
- Gagal: ubah ke Private dulu, ulangi cek.

### GH-2. Keadaan repo lokal dan identitas
```bash
cd /home/vboxuser/gemma4-agent
git rev-parse --is-inside-work-tree 2>/dev/null || git init
git config user.name  "<NAMA>"
git config user.email "<EMAIL-NOREPLY-GITHUB>"   # disarankan alamat noreply GitHub
```

### GH-3. `.gitignore` (idempoten; aman dijalankan berulang)
```bash
touch .gitignore
[ -n "$(tail -c1 .gitignore)" ] && echo >> .gitignore
while IFS= read -r l; do
  grep -qxF -- "$l" .gitignore || printf '%s\n' "$l" >> .gitignore
done <<'EOF'
# Aset kompetisi & lingkungan lokal (DILARANG PUSH)
data/
docker/
sandbox/
sample_submission/
tasks.jsonl
HARNESS_README.md
*.jsonl
.venv/
*.zip
*.tar.gz
*.safetensors
traces/
__pycache__/
.pytest_cache/
.kaggle/
# Kredensial
.env
*.env
credentials.json
kaggle.json
access_token*
*.pem
*.key
EOF
cat .gitignore
```
Catatan: pola tanpa awalan `/` berlaku di semua kedalaman. Bila ada folder sah bernama `data/`, `docker/`, atau `sandbox/` di dalam `docs/` atau `submission_root/`, ubah polanya menjadi berawalan `/`. Posisi aset kompetisi di VPS [U]: sesuaikan polanya setelah `ls` direktori proyek.

### GH-4. Staging & audit sebelum commit
```bash
git add .gitignore docs/
git status --short

# Audit nama berkas: harus mencetak "OK"
git diff --cached --name-only | grep -Ei '(^|/)(data|\.venv|traces|\.kaggle|docker|sandbox|sample_submission)/|\.(zip|tar\.gz|safetensors|jsonl)$|credentials|access_token|kaggle\.json|\.env|\.pem$|\.key$' \
  && echo "STOP: berkas terlarang ada di staging" || echo "OK: staging bersih"

# Audit isi: tinjau manual setiap baris yang muncul
git diff --cached | grep -Ein 'token|secret|password|api[_-]?key|BEGIN .*PRIVATE' || echo "OK: tidak ada pola kredensial"
```
**Tinjau `docs/ROLE.md`:** berkas ini berisi kutipan `HARNESS_README.md`, yang termasuk materi kompetisi. Di repo privat tim ini dapat diterima [A], tetapi bila ROLE.md memuat salinan penuh/bagian panjang berkas harness, keluarkan dari commit pertama (`git restore --staged docs/ROLE.md`, tambahkan ke `.gitignore`) sampai V-01 mengonfirmasi bunyi aturan.

### GH-5. Commit dan push
```bash
git commit -m "docs: lock MASTER PRD v3.4, ROADMAP v3.3, and ROLE v2.0"
git branch -M main
git remote add origin https://github.com/005-rgb/Project-JOBEN-Gemma4.git 2>/dev/null \
  || git remote set-url origin https://github.com/005-rgb/Project-JOBEN-Gemma4.git
git push -u origin main
```
- Autentikasi: *fine-grained personal access token* terbatas pada repo ini (izin Contents: read/write) atau SSH deploy key; masukkan lewat prompt/credential helper. **Jangan** menaruh token di URL remote (tersimpan di `.git/config`) dan jangan menyimpannya di direktori proyek.
- Bila ditolak karena repo sudah berisi commit awal (mis. README): `git pull --rebase origin main`, lalu `git push`. **Jangan** `--force`.

### GH-6. Verifikasi pasca-push
```bash
git ls-files                       # hanya .gitignore dan docs/*
git ls-remote --heads origin       # cabang main ada
git status --short                 # data/ dan .venv/ tidak muncul
```
Ulangi cek incognito GH-1 (harus tetap 404).

---

## 6. Aturan commit selanjutnya

| Jalur | Boleh di-commit? | Catatan |
| :-- | :-- | :-- |
| `docs/` (PRD, ROADMAP, ROLE) | Ya | ROLE.md lihat GH-4 |
| `submission_root/` (`agent.yaml`, `eval_config.yaml`, `configs/`, `prompts/`, `sub_agents/`, `skills/funnel/`) | Ya, mulai G0 | Kode agen; tanpa `.zip` |
| `tools/` (skrip build di luar arsip), unit test `funnel.py` | Ya, mulai F2 | |
| `experiments/LOG.md` | Ya | Hanya hash, konfigurasi, angka agregat (template §7) |
| Keluaran per tugas (`traces/`, ATIF, JSON per tugas, teks isu/patch referensi) | **Tidak** | Memuat konten tugas; simpan lokal |
| `data/`, `docker/`, `sandbox/`, `sample_submission/`, `HARNESS_README.md`, `*.jsonl` | **Tidak** | Aset kompetisi |
| `.venv/`, `*.zip`, `*.tar.gz`, `*.safetensors`, cache | **Tidak** | |
| `~/.kaggle/*`, token, `.env` | **Tidak, selamanya** | Di luar proyek; jangan disalin ke dalamnya |

Tag per submission:
```bash
Z=<path/ke/submission.zip>
H=$(sha256sum "$Z" | cut -d' ' -f1)
git tag -a "s1-${H:0:12}" -m "S1 Varian 0; zip sha256 $H"
git push origin "s1-${H:0:12}"
```
Tag hanya menandai kode; zip dapat direproduksi hanya bila proses build deterministik [A].

---

## 7. Template `experiments/LOG.md` [A]

| Tanggal (WIB) | Submission | Commit | Tag | sha256 zip | Konfigurasi singkat | Hasil agregat (tanpa teks tugas) |
| --- | --- | --- | --- | --- | --- | --- |
| 18 Nov 2026 | S1 | `<hash>` | `s1-<12>` | `<sha256>` | Varian 0, E4B, `max_time_minutes: 4` | – |

---

## 8. Risiko tambahan (lanjutan register PRD §13)

| Risiko | Dampak | Mitigasi |
| :-- | :-- | :-- |
| Repo publik atau berkolaborator di luar tim | Diskualifikasi | GH-1 sebelum push; cek ulang di GH-6 dan tiap awal fase. Bila terlanjur publik: jadikan Private segera, bersihkan riwayat (`git filter-repo`), baru tinjau Rules |
| Aset kompetisi atau kredensial ikut ter-commit | Diskualifikasi / kebocoran akun | `.gitignore` GH-3, audit GH-4, `git ls-files` GH-6 |
| ROLE.md memuat kutipan panjang harness | Pelanggaran pembagian data | Tinjau di GH-4; keluarkan bila ragu |
| Urusan repo menahan G0 | S1 lewat 19 Nov 06:59 WIB | Batas ≈30 menit untuk F0.0; GH bukan syarat G0 |

---

## 9. Usulan sinkronisasi PRD (v3.5, belum diterapkan)

- §14: tambah kriteria 15: "Repositori GitHub berstatus Private terverifikasi; `git ls-files` tidak memuat data kompetisi, kredensial, atau zip; tiap submission punya tag berisi hash zip."
- §13: tambah empat baris risiko dari §8 dokumen ini.
- §11: ganti baris F0 dengan baris F0 di §3 dokumen ini.
