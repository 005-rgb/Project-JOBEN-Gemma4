# ROADMAP v3.4 Terpadu: Project NS-Gemma4

Rabu 18 Nov 2026 · acuan utama: MASTER PRD v3.4 · menggantikan ROADMAP v3.2 · semua waktu WIB kecuali ditulis UTC

## 0. Dasar dan aturan penyelesaian konflik

**Sumber.** MASTER PRD v3.4 (acuan utama), ROADMAP v3.2 (rincian tugas; ID F0.x sampai F5.x dipertahankan), MASTER PRD v3.2 (hanya konteks). Bila dua sumber bertentangan, PRD v3.4 menang. Setiap konflik dan keputusannya dicatat di §10.

**Legenda.** \[V\*\], \[K\], \[A\], \[U\] sama dengan legenda PRD v3.4. **\[R\]** = keputusan penyelesaian yang dibuat roadmap ini untuk menutup celah antar-dokumen; bukan fakta dari sumber, tidak mengubah PRD, dan boleh diganti bila V-test menunjukkan lain.

**Aturan tetap.**

1. Tidak ada modul masuk submission sebelum V-test relevan lulus.
2. Angka berlabel \[K\] atau \[A\] tidak menjadi dasar keputusan tanpa V-test lulus (§14 no. 13).
3. Satu perubahan per percobaan atau lengan.
4. Keputusan hanya dari aturan §2.4 dan §10 PRD, bukan dari satu skor leaderboard (set publik 58 tugas, sangat berisik \[K\]).
5. Setiap kiriman dicatat: hash zip, konfigurasi, jam kirim, jam hasil, skor, versi PRD.
6. Setiap zip divalidasi dengan compiler resmi dan `package_and_validate.py` sebelum dikirim.

**Batas dokumen.** Penyusunan ini tidak menjalankan kode atau pencarian web. Semua ambang adalah \[A\]. "100% selesai" adalah ukuran proses, bukan skor; skor di set privat tidak bisa dijamin.

## 1. Definisi 100% selesai (14 kriteria PRD v3.4 §14)

| § 14 | Butir | Dibuktikan di | Bukti yang disimpan |
| :-- | :-- | :-- | :-- |
| 1 | Root config tunggal di root zip, lolos compiler resmi, satu string model di semua YAML, hanya 4 field `evaluation:` | F0 dan tiap submit | log compiler + `package_and_validate.py` |
| 2 | Arsip < 3 GiB, ekstensi sah, tanpa symlink, dibuat ke `/kaggle/working/submission.zip` | F0 dan tiap submit | `unzip -l` + hash zip |
| 3 | Diff bersih pada ≥10 tugas dev: 0 berkas sampah, 0 perubahan berkas terproteksi | F1 (Varian 0), F3 (lengan lain) | `git status --short` + `git diff --stat` per tugas |
| 4 | Bootstrap p99 `O + S(L)` ≤ 39600 s pada skenario (a) dan (b), dan ekstrapolasi penuh ≤11 jam | F1, lalu F3 dan F4 | keluaran bootstrap M15 |
| 5 | Seluruh metrik §9 di bawah ambang pada run konfirmasi | F3, F4 | tabel M12 |
| 6 | ≥7 dari 8 fixture adversarial lulus | ditulis di F1.6; lulus di F3.2 (Skenario B) atau F4.2/F4.3 (Skenario A) | 8 fixture + hasil |
| 7 | Komponen di luar Varian 0 lolos §10 (Tier-C/S); Varian P juga lolos §2.4 | F2, F3 | jurnal `Δ̂`, `LB80` |
| 8 | Final B memakai `e4b` (atau `e2b`) dan terpilih sebagai satu dari 2 final | F4, F5 | pilihan final |
| 9 | Submission #1 = Varian 0 murni, tanpa skrip/sub-agen, `max_time_minutes ≤ 4` | F0 | zip S1 |
| 10 | Varian P: matriks `Patch × Test` dan alasan pilihan per tugas di ATIF; diff akhir dari `funnel.py` atau cadangan tercatat; 0 berkas sampah | F3 | ringkasan `funnel.py` di ATIF |
| 11 | V-01 lulus; semua tanda `*` pada fakta yang dipakai dihapus; status \[U\] terverifikasi | F0 | daftar selisih + PRD diperbarui |
| 12 | V-31 terjawab; skenario F4 (A atau B) terkunci | F1 (G1) | catatan antrean S1/S2 |
| 13 | Tidak ada klaim \[K\]/\[A\] dipakai sebagai dasar keputusan tanpa V-test lulus | semua fase | jurnal keputusan |
| 14 | Final A dan Final B sudah selesai dinilai saat dipilih | F5 | tangkapan layar Kaggle |

## 2. Tanggal keras

| Batas | WIB | Status |
| :-- | :-- | :-- |
| S1 masuk antrean | sebelum Kamis 19 Nov 06:59 | target G0 |
| Join / merger | Kamis 26 Nov 06:59 (25 Nov 23:59 UTC); status akun `Joined` adalah \[U\] | \[V\*\]; \[U\] |
| Kandidat final terakhir | Minggu 29 Nov 18:00 (18:00 + 81 jam = Kamis 3 Des 03:00) | turunan angka 81 jam \[K\] |
| Batas final dan pilih 2 final | Kamis 3 Des 06:59 (2 Des 23:59 UTC) | \[V\*\] |
| Total sesi evaluasi | maks 12 jam; target aman ≤11 jam (`H` = 39600 s) | \[V\*\]/\[K\] |

Hari submission diasumsikan berganti pada 00:00 UTC = 07:00 WIB \[K\]. Contoh: "hari" S1 berjalan Rabu 18 Nov 07:00 sampai Kamis 19 Nov 06:59. Diverifikasi di V-31. Pemilihan dua final dijadwalkan **Rabu 2 Des sebelum 18:00** \[R\] (margin ≥12 jam dari batas).

## 3. Gambaran fase

| Fase | Tanggal | Tujuan | Gerbang |
| :-- | :-- | :-- | :-- |
| F0 | Rab 18 | Verifikasi status, berkas resmi, Varian 0 valid, S1 terkirim | G0 |
| F1 | Rab 18 – Jum 20 | Dev set, benchmark, telemetri, `L`, S2 dan V-31 | G1 |
| F2 | Kam 19 – Min 22 | V-test Funnel, `funnel.py`, diagnosis §2.4 | G2 (GO/NO-GO) |
| F3 | Sen 23 – Rab 25 | Saringan R=1, konfirmasi R=3, S3 | G3 |
| F4 | Skenario A: Kam 26 – Min 29. Skenario B: pembekuan Rab 25, S4 paling lambat Kam 26 09:00 | Pembekuan dan kiriman final | G4 |
| F5 | Sen 30 Nov – Rab 2 Des | Pantau antrean, hotfix format, pilih 2 final | G5 = selesai |

F1 dan F2 tumpang tindih di 19–20 Nov (disengaja: V-test Funnel hanya butuh kernel dev dan `agent.yaml` contoh).

## 4. Rincian fase

### F0 · Rabu 18 Nov: fondasi dan Submission #1

| ID | Tugas | Bukti | Est. |
| :-- | :-- | :-- | :-- |
| F0.1 | Verifikasi status `Joined` \[U\]; bila belum, Join dan setujui aturan sekarang | halaman Kaggle | 0,1 j |
| F0.2 | Unduh `HARNESS_README.md`, `tasks.jsonl`, `sample_submission`, wheelhouse `swegemma`; cek sisa kuota GPU | berkas lokal; catatan kuota | 0,5 j |
| F0.3 | **V-01**: cocokkan ROLE.md dengan `HARNESS_README.md` asli; hapus `*` per baris yang cocok | daftar selisih | 1 j |
| F0.4 | **V-06, V-07, V-12**: 4 field `eval_config`; sintaks `agent.yaml` (`SequentialAgent`, `ParallelAgent`, `output_key`, `agent_tool`, `!include`, escape kurung kurawal); ekstensi sah | catatan sintaks terbukti | 1,5 j |
| F0.5 | **V-10, V-11**: struktur `tasks.jsonl`, nama field patch referensi dan `test_patch`, ukuran set publik | skema field | 0,5 j |
| F0.6 | Tulis Varian 0: `agent.yaml`, `prompts/system.md` (≤1,2k token + playbook ≤600), `eval_config.yaml` = `timeout_seconds 120 / max_tool_calls 30 / max_time_minutes 4 / max_turns 40`, `configs/sampling.yaml` = `temperature 0.2`, `max_output_tokens 6144`, `thinking_budget 2048`, `include_thoughts false` | `submission_root/` | 2,5 j |
| F0.7 | Validasi: compiler resmi + `package_and_validate.py`; satu nama model di semua YAML; tanpa YAML nganggur | log lolos | 0,5 j |
| F0.8 | Smoke `swegemma eval` 3–5 tugas: patch terbentuk, tanpa berkas sampah, `submit_patch` terpanggil | 3–5 jejak ATIF | 1 j |
| F0.9 | Model S1 mengikuti §2.3: model terbesar yang mengirim diff valid pada ≥90% dari ≥10 tugas dev dengan `max_time_minutes: 4`. Data itu belum ada di F0, sehingga **S1 = `gemma-4-e4b-it-qat-w4a16-ct`** | model tercatat | 0,2 j |
| F0.10 | **Kirim S1**; catat jam kirim dan jam hasil | zip + hash + log antrean | 0,5 j |

**G0** lolos bila F0.1 dan F0.7 selesai serta S1 antre sebelum Kam 19 Nov 06:59. Jika terlambat: smoke dipotong jadi 3 tugas dan playbook minimum; S1 tetap dikirim.

### F1 · 18–20 Nov: fondasi terukur

| ID | Tugas | Bukti | Est. |
| :-- | :-- | :-- | :-- |
| F1.1 | **Gold-check §10.1** pada 129 tugas publik: patch referensi + `test_patch` di snapshot bersih, perintah verifikasi resmi 2×; simpan hanya gold 2/2, `FAIL_TO_PASS` gagal di kode asli, tanpa `skipped`, tanpa jaringan. Target **dev M ≥ 30** seimbang antar-repo + **10 hold-out** (lantai mutlak M ≥ 24, lihat §7) | daftar tugas dev | 3–4 j |
| F1.2 | **Benchmark §2.3** pada 31B, 12B, E4B (QAT persis): konkurensi 1, 3, 4, 10; prompt 8k/output 1k; ulangi dengan 10 permintaan berprefiks bersama | tokens/s, TTFT, KV cache, hit rate prefix cache, latensi p50/p90 | 2 j |
| F1.3 | **V-14, V-18, V-19, V-20, V-24** | tabel hasil | 2 j |
| F1.4 | **V-02, V-03**: `run_skill_script` bisa Python dan baca/tulis `/workspace`; sintaks argumen; overhead dan apakah terhitung tool call | jawaban; menentukan nasib `funnel.py` (jika gagal: §5.5 PRD) | 1 j |
| F1.5 | M12 telemetri: waktu per fase, call, `edit_not_found`, ukuran diff, diff kosong, berkas sampah, token thinking | skrip + JSON per tugas | 2 j |
| F1.6 | Delapan fixture adversarial §9 | 8 fixture + kriteria lulus | 2 j |
| F1.7 | **Run baseline lebar**: Varian 0 di dev, batas 10 menit, ≥30 tugas, R=1 | `t_i` per tugas; metrik §9 | 2–3 j GPU |
| F1.8 | **M15**: bootstrap ≥10.000 resampel pada dua skenario ((a) N=120 ×1,0; (b) N=150 ×1,2); `L` bulat terbesar dengan 4 ≤ L ≤ 10 dan p99 ≤ `H`. Tanpa data: `L_safe` = 4 menit | `L` tercatat | 1 j |
| F1.9 | Perbaikan baseline (hanya Tier-S) lalu **kirim S2** (Varian 0 + `L`) | zip S2 | 2 j |

**G1 (Jum 20, 22:00) memutuskan tiga hal:**

1. **V-31 dan skenario F4.** Jawab: apakah ≥2 submission boleh pending, kapan reset harian, berapa durasi antrean S1/S2. Percobaan mengirim S2 saat S1 masih pending menguji aturan "1 pending".
   - ≥2 pending: **Skenario A**. Bila antrean 24–48 jam, S3 wajib sudah sekelas kandidat final dan S5 dikirim paling lambat Sab 28 Nov \[R, dari ROADMAP v3.2\].
   - 1 pending ketat, atau antrean ≥48 jam: **Skenario B** (§6).
2. **Status 12B.** V-24 gagal atau benchmark menunjukkan 12B tak sanggup di bawah `L`: coret 12B.
3. **Status 31B + P.** Perhitungan kasar \[A\]: kebutuhan KV ≈60k vs KV 31B ≈46k \[K\], sehingga 31B + P gugur kecuali pengukuran F1.2 menunjukkan sebaliknya.

### F2 · 19–22 Nov: kelayakan Funnel

| ID | Tugas | Bukti | Est. |
| :-- | :-- | :-- | :-- |
| F2.1 | **V-15, V-16, V-17**: root `SequentialAgent` + terminasi `submit_patch` + nudge; pengaruh call/giliran sub-agen pada `max_tool_calls`/`max_turns`; `{localization}` terisi dan konteks sub-agen terpisah | hasil; rung fallback dipilih | 3 j |
| F2.2 | **V-25** (prefix cache), **V-27** (jembatan J1: `write_file` per cabang, payload tak terpotong, kandidat bisa dipulihkan dari ATIF), **V-30** (sintaks dan batas 10 `sub_agents`; prefiks identik) | hasil; J1 atau J2 | 3 j |
| F2.3 | **V-26** (impor dari `/workspace`), **V-23** (pulih dari byte asli), **V-28** (tanpa `__pycache__`/`.pytest_cache`), **V-21** (konfigurasi/fixture repo untuk tes di `/tmp/cand`), **V-29** (JUnit XML + `--tb=short` cukup untuk `type`, `message`, frame terdalam) | hasil; lokasi tes | 3 j |
| F2.4 | Tulis `skills/funnel/scripts/funnel.py` sesuai 8 langkah §3.3 PRD v3.4 (rincian di bawah); uji lokal pada 5 tugas dev dengan kandidat tulisan tangan | skrip + log | 5 j |
| F2.5 | Tulis `funnel_common.md`, `localizer.md`, `applier.md`, dan skrip build yang menghasilkan `branch_test_{a..d}.md` dan `branch_prop_{a..f}.md` (prefiks identik + dua baris penutup unik; skrip build di luar arsip karena `.py` hanya boleh di `skills/`); aturan penamaan N (M13); ≤1k token tetap per agen | prompt | 3 j |
| F2.6 | Susun `agent.yaml` + `sub_agents/` (`localizer`, `applier`, `branches`, 10 YAML cabang) Varian P dengan `eval_config` P = `120 / 35 / 4 / 50` (nilai `max_time_minutes` ditentukan ulang oleh M15 dan §2.4); validasi compiler | zip uji | 2 j |
| F2.7 | **Diagnosis offline M12** pada dev E4B dengan P = 6: `pass@1`, `pass@6 oracle`, `selection_accuracy`, waktu end-to-end | tabel gerbang | 4–6 j GPU |

**Spesifikasi `funnel.py` yang dipegang (PRD v3.4 §3.3).** Pustaka standar; argumen berdefault `--workdir /workspace --cand /tmp/cand --deadline-seconds 90`; invarian `deadline ≤ timeout_seconds − 30`; langkah 1–4 ≤ 0,4·D, langkah 5–8 sisanya; semua pytest serial; tanpa akses isu atau state ADK. Klasifikasi tes saringan berbasis frame terdalam; `TARGET_TESTS` repo ikut dipakai sebagai tes reproduksi; penjaga regresi dari `NEIGHBOR_TESTS` atau auto-discovery (max 2 berkas per `FILES`); seleksi CodeT dengan `diff_lines == 0` gugur; pembersihan hanya path untracked (`??`) yang tidak ada di rekaman awal. `applier`: `get_status` dulu; sisa waktu ≥150 dtk gunakan perintah tanpa argumen, bila lebih kecil gunakan templat `--deadline-seconds 40` \[A\]; `submit_patch` di turn tersendiri; cadangan `prop_a` bila `chosen: null` atau `abort_isolation`.

**G2 (Min 22, 22:00): GO bila semuanya benar.**

| Uji | Ambang |
| :-- | :-- |
| `pass@6 oracle / pass@1` | ≥ 1,4 \[A\] |
| `selection_accuracy` | ≥ 0,4 \[A\] |
| Waktu end-to-end | `t_lok + t_paralel + t_funnel + t_submit ≤ 60·L − cadangan(§4.3)` |
| Throughput agregat konkurensi 3 / konkurensi 1 | ≥ 2,0 \[A\] (V-18) |
| KV cache | ≥ 1,5 × kebutuhan fase paralel |
| V-15, V-17, V-19, V-25, V-26, V-27, V-28, V-29, V-30 | lulus |

Waktu gagal: turunkan (T,P) satu langkah dari (4,6), usulan (3,4) \[A\], ukur ulang **sekali**; bila tetap gagal, buang P.

**Tangga fallback:** V-15 gagal → Rung 1 (root `LlmAgent` memanggil `agent_tool` → `ParallelAgent`, lalu `funnel.py`; hanya menjawab masalah Sequential/terminasi, karena Rung 1 tetap memakai `ParallelAgent`). V-27 gagal → J2. Masalah `ParallelAgent` → Rung 2 (satu `LlmAgent` batch-writer, ≤8 giliran \[A\]). Semua gagal, atau tangga habis sebelum Sab 21 Nov 22:00 → Rung 3: **buang P**, jalur menjadi Varian 0 + perbaikan Tier-S (M13, M7, playbook).

**Varian S** (M1–M4) dibekukan. Dibuka kembali hanya bila P ditutup, V-02/V-03 lulus, dan waktu ada; jendela 23–25 Nov, tidak boleh mengganggu jalur kritis; bila belum lolos Tier-C di R=1 pada Rab 25 12:00, tutup permanen \[R\].

### F3 · 23–25 Nov: konfirmasi lengan

| ID | Tugas | Bukti |
| :-- | :-- | :-- |
| F3.1 | **Saringan R=1** pada dev penuh per lengan hidup; buang bila `Δ̂ < −0,05` atau V-test terkait gagal (≈1,5 j GPU/lengan) | tabel saringan |
| F3.2 | **Konfirmasi R=3** (R=4 bila perbatasan) hanya untuk yang lolos; urutan lengan diacak antar-run; seed bervariasi; `p_i`, `Δ̂`, `LB80` (bootstrap berpasangan 10.000) (≈4,5 j GPU/lengan; rencanakan 4–5 lengan) | `p_i`, `Δ̂`, `LB80` |
| F3.3 | Daftar lengan: (i) E4B + Varian 0 + Tier-S; (ii) E4B + P bila G2 GO; (iii) 12B + Varian 0 bila G1 lolos; (iv) 12B + P hanya bila (ii) menang dan benchmark mendukung (P2) | daftar final |
| F3.4 | **Kirim S3** bila aturan antrean mengizinkan: kandidat terbaik sementara | zip S3 |
| F3.5 | Re-bootstrap M15 dengan waktu lengan pemenang; tetapkan `L` final per varian | `L` final |
| F3.6 | Rabu pagi: pastikan status `Joined` masih benar sebelum Kam 26 Nov 06:59 | tangkapan layar |

**Aturan terima (PRD §10.3).** Tier-C (Varian P, ganti model, thinking lebih besar): `Δ̂ ≥ +0,03` **dan** `LB80 > 0` **dan** semua pagar. Tier-S (prompt tanpa biaya): `Δ̂ ≥ 0` dan semua pagar. Inkonklusif (`Δ̂ > 0`, `LB80 ≤ 0`) = tolak. **Pagar:** ekstrapolasi ≤11 jam; empty-patch tidak naik >3 poin persentase; over-budget ≤5%; regresi tes lama tidak naik; metrik §9 di bawah ambang. Dengan M≈30, `LB80 > 0` biasanya menuntut `Δ̂ ≈ +0,05` \[A\].

**G3 (Rab 25, 22:00):** pemenang memenuhi Tier-C/S.

### F4 · pembekuan dan kiriman final

Skenario dikunci di G1 oleh V-31. Rinciannya di §6.

### F5 · 30 Nov – 2 Des: penyangga dan pemilihan

| ID | Tugas | Bukti |
| :-- | :-- | :-- |
| F5.1 | Pantau antrean dan skor; **tanpa eksperimen baru** | log harian |
| F5.2 | Bila kiriman ditolak (`ParticipantVisibleError`, ekstensi, ukuran) dan antrean masih memungkinkan, kirim ulang hanya perbaikan format | zip hotfix |
| F5.3 | **Rab 2 Des sebelum 18:00: pilih tepat 2 final** di Kaggle dari submission yang sudah selesai dinilai; periksa pilihan tersimpan | tangkapan layar |
| F5.4 | Kepatuhan: tak ada data kompetisi di repo publik; tak ada kode privat dibagikan; arsip hanya berkas dan ekstensi sah | lembar kepatuhan |

**G5 = selesai:** 14 kriteria §14 terpenuhi, margin ≥12 jam sebelum Kam 3 Des 06:59.

## 5. Jalur kritis

F0.1 → F0.5 (V-10) → F1.1 → F1.7 → F1.8 → F3.5. Paralel: F0.4 (V-07) → F0.6 → F0.10 (S1) → data antrean → G1. Funnel: F1.3 (V-19/V-18) dan F1.2 → F2.1..F2.3 → F2.4 → F2.7 → G2 → F3 → G3 → F4 → G4 → F5.3. Dua hal yang dikerjakan lebih dulu: **F1.1 → F1.7 → F1.8** (tanpa dev set tidak ada pengukuran) dan **F2.1 → F2.2** (bila nudge atau jembatan J1 gagal, Funnel mati sebelum ditulis).

## 6. Fase F4: dua skenario (diputuskan di G1 oleh V-31)

### Skenario A: ≥2 submission boleh pending

| ID | Tugas |
| :-- | :-- |
| F4.1 | **Kam 26**: putuskan dan bekukan. Final A = pemenang §10 di antara {31B, 12B (bersyarat)} × {Varian 0, P} (atau E4B + P bila mengalahkannya); Final B = pemenang §10 di antara {E4B} × {Varian 0, P}. Simpan hash dan konfigurasi. Nol perubahan setelahnya kecuali format |
| F4.2 | Stabilitas Final A: run dev ≥30 tugas dengan `L` final; bootstrap p99 pada skenario (a) dan (b); ekstrapolasi ≤11 jam; fixture ≥7/8; 0 berkas sampah |
| F4.3 | Sama untuk Final B (E4B); boleh memakai ulang waktu F3.2 bila konfigurasi tidak berubah |
| F4.4 | Daftar periksa §14 butir 1–14 per kandidat dengan bukti |
| F4.5 | **Jum 27: kirim S4 (Final A). Sab 28: kirim S5 (Final B).** Dua hari berbeda (1/hari \[K\]) |
| F4.6 | Sampai **Min 29 18:00**: bila ditolak karena format, perbaiki hanya itu dan kirim ulang. Setelah 18:00 tidak ada kiriman yang dianggap kandidat final |

Bila Final A dan B ternyata identik (E4B menang keduanya), S4 dan S5 boleh E4B yang sama.

### Skenario B: 1 pending, serial

Dua kiriman final baru tidak muat. Batas kirim S4 = 29 Nov 18:00 − 81 jam = **Kam 26 Nov 09:00**; kode Final A dibekukan **Rabu 25 Nov**. **Hanya satu kiriman final baru; Final B diambil dari submission yang sudah selesai dinilai.**

Penyelesaian jadwal \[R\], karena F4.2 tidak boleh dipotong tetapi G3 baru Rab 25 22:00:

- **F3.2 sekaligus menjadi bukti stabilitas Final A.** Pada Skenario B, run konfirmasi lengan pemenang memakai `L` final dan memuat: ≥30 tugas dev, bootstrap p99 pada skenario (a) dan (b), ekstrapolasi ≤11 jam, fixture ≥7/8, 0 berkas sampah. Syarat: konfigurasi tidak berubah setelah G3 dan `L` tidak berubah setelah F3.5. Bila `L` berubah, ulang bootstrap dan, bila waktu masih ada, run singkat sebelum Kam 26 09:00.
- **S4 dikirim antara Rab 25 22:00 dan Kam 26 09:00** (jendela ≈11 jam).
- **Final B** = submission E4B yang sudah bernilai. S1 adalah E4B (F0.9), sehingga menjamin kandidat Final B bernilai bila S1 sudah dinilai. S3 (bila E4B dan sudah dinilai) boleh menggantikan.
- **Kiriman S2 dan S3** hanya dikirim bila kiriman sebelumnya sudah selesai dinilai dan hasilnya akan selesai sebelum S4 harus dikirim. Bila tidak muat, lewati; S4 langsung Final A. S2 pada G1 sudah harus memuat Final B sekelas kandidat (ROADMAP v3.2 G1, antrean ≥48 jam).

Pada kedua skenario, 2 final dipilih dari submission yang sudah selesai dinilai; submission yang masih tertahan antrean bukan kandidat final yang aman.

## 7. Aturan potong (stop-loss)

| Pemicu | Tindakan |
| :-- | :-- |
| S1 belum terkirim 19 Nov 06:59 | Playbook minimum, smoke 3 tugas, kirim |
| Dev set < 30 tugas gold-lolos (tetapi ≥24) pada 20 Nov | Lanjut dengan tugas yang ada; catat sebagai penyimpangan kriteria "≥30 tugas" |
| Dev set < 24 | Longgarkan keseimbangan antar-repo (tetap gold 2/2) dan catat bias |
| V-24 gagal atau 12B lambat | Coret 12B |
| V-19 menunjukkan harness paralel | Coret Varian P |
| V-15 dan semua rung gagal; V-27: J1 dan J2 gagal; V-26 gagal setelah `PYTHONPATH=/workspace` | Coret Varian P |
| Gerbang §2.4 gagal | NO-GO; jalur Varian 0 + Tier-S |
| Waktu funnel melebihi formula §2.4 | Turun satu langkah (3,4) \[A\], ukur ulang sekali, lalu buang |
| Bootstrap p99 > `H` | Kecilkan `L` satu menit, ulang F3.5 |
| Ekstrapolasi mendekati 11 jam | Kecilkan `max_time_minutes`; jangan menaikkan `H` |
| Kiriman ditolak (`ParticipantVisibleError`) | Perbaiki format saja, kirim ulang sebelum G4 |
| Kuota GPU habis | Urutan pemotongan di §8 |

## 8. Anggaran GPU \[A\]

| Item | Jam GPU |
| :-- | :-- |
| Benchmark F1.2–F1.3 | 2–3 |
| Gold-check F1.1 (sebagian besar CPU) | 1–2 |
| Baseline lebar F1.7 | 2–3 |
| Diagnosis Funnel F2.7 | 4–6 |
| Saringan R=1 (≈2 lengan) | 3 |
| Konfirmasi R=3 (4,5 j per lengan) | ≤18 untuk 4 lengan; ≤22,5 untuk 5 lengan |
| Stabilitas F4.2–F4.3 (Skenario B: terserap di F3.2) | 6–8 |
| **Total** | **≈36–43** (4 lengan); **≈40,5–47,5** (5 lengan) |

Periksa kuota di F0.2. Bila kuota kurang, urutan pemotongan: (1) lengan 12B + P; (2) saringan R=1 diperkecil ke subset; (3) F4.3 memakai ulang waktu F3.2 bila konfigurasi tidak berubah. **Jangan memotong F4.2.**

## 9. Buku kiriman

| Slot | Skenario A | Skenario B | Isi | Syarat kirim |
| :-- | :-- | :-- | :-- | :-- |
| S1 | Rab 18 | Rab 18 | Varian 0, E4B, `max_time_minutes: 4` | G0 |
| S2 | Jum 20 | setelah S1 dinilai, bila muat | Varian 0 + `L` + Tier-S (B: sekelas kandidat Final B) | F1.8 selesai |
| S3 | Sel 24 | opsional, bila muat | Kandidat terbaik sementara | F3.1 selesai |
| S4 | Jum 27 (Final A) | Rab 25 22:00 – Kam 26 09:00 (Final A) | Final A terbeku | G3 (+ F4.2) |
| S5 | Sab 28 (Final B) | tidak ada; Final B dari submission bernilai | Final B (E4B) | G3 + F4.3 |
| Cadangan | Min 29 – Sel 1 Des | idem | hanya perbaikan format | S4/S5 ditolak |

## 10. Konflik antar-dokumen dan keputusan

| Butir | ROADMAP v3.2 / PRD v3.2 | PRD v3.4 | Keputusan |
| :-- | :-- | :-- | :-- |
| Kriteria selesai | 10 butir | 14 butir | 14 butir (§1) |
| Join | F0.1 "Join malam ini" | `Joined` adalah \[U\] | Verifikasi dulu (F0.1) |
| Gerbang G2 | V-15/17/19/25/26/27/28; waktu `≤ L` | Tambah V-29, V-30; formula waktu dengan cadangan; gerbang KV | PRD v3.4 (G2) |
| `funnel.py` deadline | `--deadline-seconds` = sisa waktu − pemicu | Default 90, invarian ≤ `timeout_seconds − 30`, dua templat `applier` | PRD v3.4 (F2.4) |
| Berkas prompt cabang | `patch_branch.md`, `test_branch.md` | `branch_test_{a..d}.md`, `branch_prop_{a..f}.md` dari skrip build di luar arsip | PRD v3.4 (F2.5) |
| Aturan antrean | dijawab di G1 dari S1 | V-31 dan Skenario A/B | G1 = V-31 |
| S4 Jum 27 dan S5 Sab 28 | jadwal tunggal | Skenario A atau B | Dua skenario (§6) |
| Stabilitas F4.2 vs pembekuan Rab 25 | F4.2 tidak boleh dipotong | Pembekuan Rab 25 pada Skenario B | F3.2 menjadi bukti stabilitas \[R\] |
| Lengan konfirmasi | ≤4 | 4–5 | Rencanakan 5 bila kuota ada (§8) |
| Dev set | M ≥ 24 (target 30–40) dan run ≥30 | M ≥ 24 (target 30–40) lalu F1: M ≥ 30 | Target 30; lantai 24; penyimpangan dicatat (§7) |
| `max_time_minutes` Varian P | 4 | 4, tetapi komentar menyebut kemungkinan ≥5 | Ditetapkan M15 dan §2.4, bukan tebakan |
| Hari submission | 07:00 WIB \[A\] | UTC \[K\] | Sama (00:00 UTC = 07:00 WIB); dicek V-31 |
| Peluang bonus kecil ≈10% | tertulis di ROADMAP | Hanya angka bersyarat 20–25%, 35–45% | Semua \[A\]; tidak dipakai memutuskan |
| Varian S | dibuka di jendela 23–25 Nov | dibekukan | Opsional \[R\], tidak di jalur kritis |

## 11. Kalender

| Tanggal | Fokus | Hasil akhir hari |
| :-- | :-- | :-- |
| Rab 18 | F0.1–F0.10; mulai F1.1 | **S1 terkirim** |
| Kam 19 | F1.1 selesai; F1.2–F1.4, F1.6; mulai F2.1 | dev set; benchmark; V-19/V-20/V-24; V-02/V-03 |
| Jum 20 | F1.5, F1.7–F1.9; F2.1–F2.2 | **S2 terkirim**; `L`; **G1** (V-31, 12B, 31B) |
| Sab 21 | F2.3–F2.6 | `funnel.py` lolos uji lokal |
| Min 22 | F2.7 | **G2 GO/NO-GO** |
| Sen 23 | F3.1 | saringan R=1 |
| Sel 24 | F3.2 (mulai), F3.4 | S3 (bila muat) |
| Rab 25 | F3.2 (selesai), F3.5, F3.6 | **G3**. Skenario B: pembekuan; mulai kirim S4 setelah 22:00 |
| Kam 26 | A: F4.1 bekukan. B: **S4 paling lambat 09:00** |  |
| Jum 27 | A: F4.2, F4.4, **S4** |  |
| Sab 28 | A: F4.3, F4.4, **S5** |  |
| Min 29 | F4.6 | **18:00: batas keras kandidat final** |
| Sen 30 – Sel 1 | F5.1, F5.2 | pantau; hanya hotfix format |
| Rab 2 Des | F5.3, F5.4 | **dua final terpilih (sebelum 18:00); G5 = selesai** |

## 12. Pertanyaan terbuka yang dijawab paling awal

1. Aturan antrean (jumlah pending, reset harian, durasi 48–81 jam \[K\]) → V-31, G1.
2. Kuota GPU Kaggle tersisa → F0.2.
3. Sintaks `agent.yaml` untuk `ParallelAgent`, `output_key`, escape kurung kurawal → V-07 (F0.4).
4. `max_time_minutes` pecahan; diff dipungut saat habis? → V-20.
5. `ParallelAgent` bekerja di SDK kompetisi? (laporan \[K\] bermasalah) → V-15 (F2.1).
6. `V-05` (auto-compaction tidak merusak `{localization}`/state cabang, P1) tidak ditempatkan di PRD maupun ROADMAP; dijalankan bersama F2.1 sebagai \[R\].
