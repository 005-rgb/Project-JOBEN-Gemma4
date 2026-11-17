# MASTER PRD v3.4: Project NS-Gemma4 (Penyempurnaan Presisi v3.3, Mandiri & Lengkap)

Nov 18, 2026 · @exe23 · menggantikan v3.3

**Kompetisi:** Google – The Gemma 4 Developer Agent Competition (Kaggle, host Google DeepMind)
**Acuan:** `ROLE.md v2.0 Audited` (kutipan `HARNESS_README.md` / `sample_submission`) · v3.2 (dasar angka dan V-tests) · ROADMAP v3.2 (**tidak tersedia di sesi penyusunan ini; setiap klaim darinya berstatus [K]**)

**Legenda kepastian (wajib di dokumen dan komentar kode):**
- **[V\*]** bersumber dari dokumen resmi sebagaimana dikutip di ROLE.md v2.0, atau diturunkan langsung dari v3.2. **Belum dicocokkan ke berkas asli** sampai `V-01` lulus. Tanda `*` dihapus per baris setelah dicocokkan.
- **[K]** laporan peserta/komunitas atau dokumen turunan yang tidak tersedia di sesi ini. Bisa usang; wajib diuji sebelum diandalkan.
- **[A]** asumsi atau hipotesis rekayasa tim. Wajib melewati gerbang uji.
- **[U]** laporan pengguna tentang lingkungan sendiri, belum diperiksa di sesi ini.

Aturan: tidak ada modul masuk submission sebelum V-test relevan berstatus lulus. Sesi penyusunan v3.4 tidak menjalankan pencarian web maupun eksekusi kode; semua angka ambang adalah [A].

---

## 00. Audit v3.3 dan Koreksi di v3.4

| # | Cacat di v3.3 | Koreksi v3.4 |
| --- | --- | --- |
| D1 | Ringkasan menyebut 7 celah, §00 menyebut 6; baris matriks tidak cocok dengan ringkasan (tangga fallback tidak punya baris) | Satu daftar 7 koreksi inti (§00.1) + koreksi tambahan D8–D22 di tabel ini |
| D2 | "`max_turns: 50` batas resmi sampel": 50 adalah **nilai** `sample_submission` (60/10/1/50), bukan batas | Ditulis sebagai nilai sampel [V\*]; kecukupan 50 adalah [A], diukur di V-16 |
| D3 | "write_file = 2 giliran LLM, 20 giliran untuk 10 cabang" dinyatakan seolah fakta | [A]. Belum diketahui apakah giliran sub-agen paralel dihitung ke `max_turns` (V-16) |
| D4 | Fallback `NAMES` "dari isu" di `funnel.py`: skrip **tidak punya akses isu** (v3.2 §00.2 #2). Klaim kemampuan fiktif | Fallback hanya dari data yang dimiliki skrip: `FILE:` di `prop_*.txt`, nama berkas, isi `spec.txt` (§3.3 langkah 2) |
| D5 | Tangga fallback: Rung 1 (`agent_tool` → `ParallelAgent`) dijadikan jawaban atas kegagalan `ParallelAgent`; Rung 1 tetap memakai `ParallelAgent`. J2 dari v3.2 hilang | Tangga dibangun ulang sebagai tabel kegagalan → tindakan (§3.3), J2 dipulihkan |
| D6 | Status akun `Joined`, aset di `/home/vboxuser/...`, `.venv/` berlabel [V] | Diubah ke **[U]**; diverifikasi lewat F0 |
| D7 | Dua final masuk antrean sebelum 29 Nov 18:00 WIB bertentangan dengan aturan "1 submission/hari, 1 pending" yang tercatat di PRD sendiri. Hitungan 81 jam hanya benar untuk satu kiriman | Dua skenario jadwal + uji V-31 (§11). Final dipilih dari submission yang sudah bernilai |
| D8 | PRD mengutip §9, §10, §14, §2.4, M11–M15, V-01..V-28, register risiko, perilaku `applier`, `eval_config` P, tetapi bagian-bagian itu tidak ada (dokumen tidak mandiri); heading 1–8 tidak cocok dengan rujukan silang | Penomoran v3.2 (§0–§14) dipulihkan; semua bagian dirujuk tersedia di dokumen ini |
| D9 | Blok YAML `eval_config.yaml` dua kolom dalam satu blok: bukan YAML valid | Dua blok terpisah (§5.2) |
| D10 | Struktur arsip hanya `branches.yaml`; `sub_agents` memakai referensi `config_path` per agen, dan tiap cabang punya `temperature`/`seed`/`instruction` berbeda. Cara menyusun 10 agen tidak terjawab | 10 YAML cabang + 10 prompt cabang hasil skrip build di luar arsip (§5.4); sintaks dipastikan di V-07, V-30 [A] |
| D11 | Filter exception dilonggarkan tanpa definisi "berasal dari `/workspace`"; penjaga `NAMES` v3.2 dibuang; `ImportError`/`NameError` hilang tanpa alasan | Aturan klasifikasi presisi berbasis frame terdalam (§3.3 langkah 3), diuji V-29 |
| D12 | Suhu `prop_a=0.15` di luar rentang 0,2–0,8 v3.2; suhu/seed tes dan nilai lain tanpa dasar | Grid linear 0,20–0,80, seed tetap; semua [A] (§3.3) |
| D13 | `--deadline-seconds` default 120 sama dengan `timeout_seconds: 120`; skrip bisa dibunuh sebelum mencetak ringkasan. Anggaran waktu fase tidak dialokasikan; 4 tes × 25 dtk saja = 100 dtk | Default 90, invarian `deadline ≤ timeout_seconds − 30`, alokasi fase, dua templat perintah `applier` (§3.3, §5.2) |
| D14 | `TARGET_TESTS` ditulis ke `spec.txt` tetapi tidak dipakai di algoritma | Dipakai sebagai tes reproduksi tambahan bila ada di repo dan gagal di baseline (langkah 3) |
| D15 | Legenda `[V]` mengesankan sudah dicocokkan ke berkas resmi | Legenda `[V*]` (di atas) |
| D16 | Gerbang KV tidak dihitung; KV 31B ≈46 ribu token [K] vs kebutuhan ×1,5 | Perhitungan kasar di §2.3: 31B + P hampir pasti gugur kecuali terukur lain |
| D17 | Prosedur `applier` dan cadangan (`prop_a` via `edit_file` bila `chosen:null`/abort) hilang | Dipulihkan (§3.3 `applier`) |
| D18 | Pembersihan "hapus berkas baru" tanpa batas | Hanya path untracked (`??`) baru yang tidak ada di rekaman awal; berkas tracked tidak pernah dihapus |
| D19 | "Waktu funnel ≤ L" membandingkan detik dengan menit tanpa definisi | Didefinisikan: `t_lok + t_paralel + t_funnel + t_submit ≤ 60·L − cadangan` (§2.4) |
| D20 | Turun ke (T,P)=(3,4) disajikan tegas | [A], satu langkah penurunan, diukur ulang 1× |
| D21 | Fixture adversarial, KPI, antrean, lisensi, batas waktu "termasuk setup sandbox" hilang dari v3.2 | Dipulihkan |
| D22 | ROLE.md menulis batas daftar "25 Nov 06:59 WIB" | Dipertahankan koreksi v3.1: 26 Nov 06:59 WIB (= 25 Nov 23:59 UTC). Wajib dicocokkan ke halaman Kaggle di V-01 |

### 00.1 Tujuh Koreksi Inti v3.2 → v3.3 (dipertahankan, dengan label diperbaiki)

| # | v3.2 | v3.3/v3.4 | Status |
| --- | --- | --- | --- |
| 1 | 10 cabang J1 tanpa path berkas unik | Dua baris penutup unik per cabang memuat path unik (`/tmp/cand/test_a..d.py`, `/tmp/cand/prop_a..f.txt`); seluruh prefiks di atasnya identik | [A] V-25, V-27 |
| 2 | `max_turns: 40`, `max_tool_calls: 30` | P: `max_turns: 50` (nilai sampel [V\*]), `max_tool_calls: 35`; `localizer` ≤5 call eksplorasi + call ke-6 menulis `spec.txt` | [A] V-16 |
| 3 | Seri CodeT = `diff_lines` terkecil tanpa cek nol | `diff_lines == 0` (OLD == NEW) gugur di langkah 2 | [A] |
| 4 | Saringan tes: `AssertionError` atau 4 exception berbasis `NAMES` | Klasifikasi berbasis frame terdalam (§3.3 langkah 3) | [A] V-29 |
| 5 | Parser kaku; `NEIGHBOR_TESTS` kosong = tanpa penjaga; argumen CLI wajib | Parser toleran; auto-discovery tes tetangga; argumen berdefault aman | [A] |
| 6 | Cadangan hanya sebagian | Tangga fallback berlapis (§3.3) | [A] |
| 7 | Jadwal final 30 Nov–1 Des | Batas kirim kandidat final paling lambat Min 29 Nov 18:00 WIB, dengan syarat antrean (D7) | [K] |

---

## 1. FAKTA KOMPETISI & KONTRAK HARNESS

| Item | Aturan | Status |
| :-- | :-- | :-- |
| Batas daftar/merger | Kamis **26 Nov 2026 06:59 WIB** (25 Nov 23:59 UTC). Akun saat ini `Joined` | [V\*]; status akun [U] |
| Batas final & pilih 2 final | Kamis **3 Des 2026 06:59 WIB** (2 Des 23:59 UTC) | [V\*] |
| Model | Tepat satu dari `gemma-4-{31b,12b,e4b,e2b}-it-qat-w4a16-ct`. `validate_single_declared_model` memindai root `agent.yaml`, semua `sub_agents[*].config_path`, `tools[*].agent_tool.config_path`, **dan setiap YAML agen mandiri di arsip** (`len(models) == 1`, jika tidak `ParticipantVisibleError`). Varian bfloat16 hanya untuk CLI lokal | [V\*] |
| LoRA | Boleh via `adapter:`; tanpa LoRA hapus field `adapter:`. Proyek ini tanpa LoRA (M10 ditutup) | [V\*] |
| Small Model Bonus ($10k) | Harus `e4b` atau `e2b` dan menjadi satu dari 2 final; tetap eligible di Main Track ($65k). 12B/31B tidak eligible | [V\*] |
| Metrik | Resolution Rate = resolved / total tugas split evaluasi, pada tes tersembunyi (`scripts/metric.py`) | [V\*] |
| Data | Publik `data/tasks.jsonl`: 129 tugas dari `fastapi`, `rich`, `requests`, `httpx`. Tersembunyi ≈120 tugas, repo Python privat | [V\*]/[K] |
| Waktu | Maks **12 jam** total sesi offline (termasuk setup sandbox, tanpa validasi patch); lewat 12 jam menggagalkan seluruh submission. Default CLI `max_time_minutes` 30 pasti melampaui | [V\*]/[K] |
| Perangkat | 4×L4 (96 GB), vLLM `tensor_parallel_size=4`, `gpu_memory_utilization=0.90`, `scheduler_reserve_full_isl=False`, internet mati. Sandbox A dan B: 4 GiB RAM, 2 vCPU | [V\*] |
| Konteks | `max_model_len = 32768` (prompt + thought + output). `EventsCompactionConfig` `compaction_interval = 15` | [V\*] |
| KV cache | 31B pada 4×L4 ≈46 ribu token total | [K] |
| 12B | Harness menyuntik `--hf-overrides '{"architectures": ["Gemma4ForCausalLM"], "model_type": "gemma4"}'` | [V\*] |
| Turn-0 | Harness menyuntik hingga 200 entri breadth-first tata letak `/workspace` (`find . -mindepth 1 -maxdepth 3`; `docs`, `docs_src`, `tests`, `examples`, `benchmarks` dipangkas di bawah kedalaman 1) | [V\*] |
| `eval_config.yaml` | Root `evaluation:`, 4 field opsional: `timeout_seconds`, `max_tool_calls`, `max_time_minutes`, `max_turns`. Sampel: 60/10/1/50. Default CLI: `--timeout-seconds 300`, `--max-tool-calls 50`, `--max-time-minutes 30`, `--verification-timeout-seconds 300` | [V\*] |
| Tool | `run_command`, `read_file`, `edit_file`, `write_file`, `get_code_neighbors`, `search_similar_code`, `get_code_subgraph`; skill: `load_skill`, `load_skill_resource`, `run_skill_script`. **Gratis:** `get_status`, `submit_patch` | [V\*] |
| `get_status()` | `status`, `tool_calls_used`, `patch_submitted`, `patch_size`, `tool_calls_remaining`, `max_tool_calls`, `time_seconds_remaining` | [V\*] |
| Tool graf | Blok instruksi graf hanya disuntik bila graf `.json` dan embedding `.npz` `> 100` byte tersedia untuk `task.repo` | [V\*] |
| Kelas agen | `LlmAgent`, `SequentialAgent`, `ParallelAgent`, `LoopAgent` (`1..500`). Field `LlmAgent`: `name`, `model`, `adapter`, `description`, `instruction`, `global_instruction`, `tools` (string / `agent_tool: {config_path, skip_summarization}` / inline), `skills`, `sub_agents` (`{config_path}`), `output_key`, `include_contents` (`default`/`none`), `disallow_transfer_to_parent`, `disallow_transfer_to_peers`, `generate_content_config`. Placeholder: `{problem_description}`, `{hints}`, `{<output_key>}` | [V\*] |
| `generate_content_config` | Boleh: `temperature`, `top_p`, `top_k`, `max_output_tokens` (1..32768, default 16384), `presence_penalty`, `frequency_penalty`, `stop_sequences`, `response_mime_type`, `seed`, `thinking_config`. Terlarang: `tools`, `system_instruction`, `http_options`, `safety_settings`, `response_schema` | [V\*] |
| `thinking_config` | Pakai `thinking_budget` (0..32768, default 4096) + `include_thoughts`. `budget > 0` + `include_thoughts: false` tetap berpikir pada turn berjalan tetapi membuang `Part(thought=True)` dari riwayat keluar. `0` = nonaktif. Jangan pakai `thinking_level` | [V\*] |
| Nudge & error | `ToolErrorPlugin` mengubah error tool jadi JSON dan mengonversi list tunggal `["x"]` → `"x"` pada `skill_name`/`file_path`. Maks 3 *continuation nudge* (`max_nudges = 3`, reset bila turn menjalankan ≥1 tool call valid); `budget_warning` | [V\*] |
| Patch | `submit_patch` menghentikan loop segera setelah turn selesai, boleh dipanggil walau call habis selama waktu ada. Ekstraksi: `git add -N .` lalu `git diff --binary _swegemma_baseline 2>/dev/null \|\| git diff --binary HEAD`. Dibuang otomatis: `test_*.py`, `*_test.py`, `.py` di `tests/`, `test/`, `testing/`, serta `conftest.py`, `pytest.ini`, `pyproject.toml`, `tox.ini`, `setup.cfg`, `.pytest.ini`, `sitecustomize.py`, `usercustomize.py`, `_swegemma_stubs.py`, `*.pth` | [V\*] |
| Lulus Fase 2 | `cd /workspace && PYTHONSAFEPATH=1 PYTHONNOUSERSITE=1 python3 -s -m pytest <targets> --junitxml=/tmp/_swegemma_junit_<id>.xml -p no:anyio -o timeout=0 -o python_classes="Test* *Test" -q` exit `0` **dan** JUnit ada, `passed_tests > 0`, `failures == 0`, `errors == 0`, node wajib lulus **tanpa `skipped`** | [V\*] |
| Arsip | Deklaratif, tanpa `agent.py`; tepat satu root config (`agent.yaml`/`agent.yml`/`root_agent.yaml`/`root_agent.yml`); `< 3 GiB` (3,221,225,472 byte) tak terkompresi; ≤10.000 file; ekstensi `.yaml .yml .md .txt .py .json .safetensors` (`.py` hanya skrip di direktori skill); tanpa symlink, `..`, path absolut | [V\*] |
| Submit | Maks 1 per hari, 1 pending, pilih 2 final. Antrean bisa tertahan 48–81 jam | [K] |
| Lisensi/data | Pemenang wajib OSI (Apache 2.0). Data kompetisi tak boleh dibagikan; berbagi kode privat di luar tim = diskualifikasi | [V\*] |
| Kalibrasi skor | Agen prompt-only ≈0,15–0,17; leaderboard publik hanya 58 tugas dan sangat berisik | [K] |

---

## 2. STRATEGI & TARGET

### 2.1 Dua jalur, dua final
- **Jalur aman:** Varian 0 (§3.1): satu `LlmAgent`, tanpa skrip, sub-agen, LoRA. **Submission #1**.
- **Jalur ambisius:** Varian P = Funnel Uji-Dulu (§3.3). Hipotesis [A]: model kecil lebih andal menulis kode sekali jalan daripada menjalankan loop 20 langkah, dan decode paralel di vLLM murah; banyak kandidat + verifikasi eksekusi deterministik lebih murah daripada memperbesar model.
- **Final A (Main Track):** pemenang §10 di antara {31B, 12B (bersyarat §2.3 dan V-24)} × {Varian 0, P}, atau E4B + P bila mengalahkannya.
- **Final B (Small Model Bonus):** pemenang §10 di antara {E4B} × {Varian 0, P}. E2B hanya cadangan.

### 2.2 KPI (diukur di dev, bukan janji)
| KPI | Final A | Final B |
| :-- | :-- | :-- |
| Patch valid dikirim | ≥95% tugas | ≥90% tugas |
| Ekstrapolasi total ≤11 jam | wajib | wajib |
| Metrik §9 di bawah ambang | wajib | wajib |
| Resolution rate dev | lolos aturan §10 vs Varian 0 | idem |

### 2.3 Benchmark infrastruktur & gerbang Varian P
Kernel dev 4×L4, model QAT persis (31B, 12B, E4B); konkurensi 1, 3, 4, 10; prompt 8k token, output 1k token; ulangi dengan 10 permintaan berprefiks bersama (§3.3). Metrik: tokens/s per aliran dan agregat, TTFT, ukuran KV cache (log vLLM), latensi turn p50/p90, hit rate prefix cache (V-25).

Gerbang infrastruktur (semua [A]):
1. Throughput agregat konkurensi 3 ≥ 2,0× konkurensi 1 (V-18).
2. KV cache ≥ 1,5 × kebutuhan fase paralel. Bila V-25 lolos: konteks bersama + bagian unik 10 cabang; bila tidak: 10 × konteks p90.
3. Harness menjalankan tugas serial (V-19). Bila paralel, Varian P gugur.

*Perhitungan kasar [A] (asumsi: konteks bersama ≈8k token; bagian unik per cabang ≈ 100 token instruksi + ≤1024 thinking + ≤2048 output ≈ 3,2k):* kebutuhan ≈ 8k + 10 × 3,2k ≈ 40k; ×1,5 ≈ 60k. KV 31B ≈46k [K] **tidak memenuhi**, sehingga 31B + P diperkirakan gugur kecuali pengukuran menunjukkan sebaliknya. E4B/12B memiliki ruang KV lebih besar karena bobot lebih kecil; wajib diukur.

Syarat 12B: lolos V-24 dan menyelesaikan tugas dalam batas `L` (§5.1).
**Model Submission #1:** model terbesar yang pada ≥10 tugas dev dengan `max_time_minutes: 4` mengirim diff valid pada ≥90% tugas [A]; bila belum terukur, pakai `gemma-4-e4b-it-qat-w4a16-ct`.

### 2.4 Gerbang pembunuh Varian P
Diukur pada dev gold-check (§10.1) untuk E4B (dan 12B bila lolos §2.3) lewat diagnosis offline M12 dengan P = 6:

| Uji | Lanjut jika | Jika tidak |
| :-- | :-- | :-- |
| `pass@6 oracle / pass@1` | ≥ 1,4 [A] | Buang Varian P |
| `selection_accuracy` | ≥ 0,4 [A] | Kembali ke Varian 0 |
| Waktu end-to-end per tugas: `t_lok + t_paralel + t_funnel + t_submit ≤ 60·L − cadangan(§4.3)` | terpenuhi | Turunkan (T,P) dari (4,6) satu langkah (usulan (3,4) [A]), ukur ulang 1×; bila tetap gagal, buang |
| V-15, V-17, V-19, V-25, V-26, V-27, V-28, V-29, V-30 | lulus | Tangga fallback §3.3; bila tetap gagal, buang |

*Hipotesis kuantitatif [A], perkiraan penulis ide, bukan data:* bila pass@1 ≈ 0,17 dan oracle@6 ≈ 0,28, pemulihan 40% selisih ≈ +0,04; peluang semua gerbang lolos ≈ 35–45%; Small Model Bonus ≈ 20–25% bila lolos. Angka ini bukan KPI dan tidak boleh dipakai memutuskan apa pun; keputusan hanya dari §2.4 dan §10.

### 2.5 Tidak dikerjakan di jalur utama
`deep_think`, M5, M8 (P2); Varian S/M1–M4 (dibekukan); M14, M10 LoRA (ditutup); perpanjangan anggaran global (dihapus).

---

## 3. ARSITEKTUR

### 3.1 Varian 0 (Submission #1 dan pembanding semua A/B)
Satu `LlmAgent`, tool bawaan, tanpa `skills`, `sub_agents`, `adapter:`. Prompt kontrak-first ≤1,2k token + playbook statis ≤600 token. Urutan tetap:
1. Baca `{problem_description}` dan peta Turn-0 (jangan `ls`/`find` tingkat atas).
2. Lokalisasi ≤6 call (`run_command` grep terarah, `read_file` ≤120 baris; `search_similar_code` hanya bila blok graf ada di prompt). Fallback bila graf tak ada: grep teks terarah.
3. Reproduksi opsional ≤2 call: tes yang disebut isu, `timeout 100 ... 2>&1 | tail -n 30`.
4. `edit_file` kecil, `old_string` ≥3 baris verbatim.
5. Satu `run_command`: `python3 -m py_compile <file>` lalu tes terarah terpangkas.
6. `git status --short`: nol berkas baru di `/workspace`.
7. `submit_patch` pada turn tersendiri (atau saat pemicu §4.3).

### 3.2 Varian S: DIBEKUKAN
M1–M4 (`edit_symbol.py`, `preflight.py`, `check.py`, `finalize.py`) tidak dikerjakan dan tidak masuk arsip. Desain tersimpan di arsip v3.2 §3.2/§7. Dibuka kembali hanya bila P ditutup oleh §2.4 dan waktu ada.

### 3.3 Varian P: Funnel Uji-Dulu

**Topologi:** root `SequentialAgent` dengan tiga tahap.

| Tahap | Agen | Tool | Keluaran |
| :-- | :-- | :-- | :-- |
| 1 | `localizer` (`LlmAgent`) | `run_command`, `read_file`, `write_file`. **Maks 5 call eksplorasi; call ke-6 wajib `write_file` ke `/tmp/cand/spec.txt`, lalu selesai** | `output_key: localization`: (a) ringkasan akar masalah, (b) `file:simbol`, (c) kutipan verbatim blok target ≤120 baris, (d) gaya tes tetangga ≤60 baris. Plus `/tmp/cand/spec.txt` |
| 2 | `branches` (`ParallelAgent`) beranggota 10 `LlmAgent`: `branch_test_a..d`, `branch_prop_a..f` | **hanya `write_file`** (jembatan J1); `include_contents: "none"` | `/tmp/cand/test_a..d.py`, `/tmp/cand/prop_a..f.txt` |
| 3 | `applier` (`LlmAgent`) | `get_status`, `run_skill_script` (atau `run_command`, §5.5), `read_file`, `edit_file`, `submit_patch` | menjalankan `funnel.py` lalu `submit_patch` |

**Format `spec.txt`** (ditulis dengan satu `write_file`, **tanpa kurung kurawal**; pemisah koma atau baris baru):
```
NAMES: nama_api_dari_isu, nama_lain
TARGET_TESTS: tests/test_x.py::test_a
NEIGHBOR_TESTS: tests/test_x.py::test_b
FILES: pkg/modul.py
```

**Prefiks bersama (V-25).** Semua 10 cabang: set tool identik `[write_file]`; instruksi berurutan `funnel_common.md` (aturan penamaan N dari M13, format keluaran, larangan) → `{problem_description}` → `{localization}` → **dua baris penutup unik**:
- Cabang tes `k ∈ {a..d}`: `MODUS: TULIS TES REPRODUKSI. Simpan hasil hanya dengan memanggil write_file ke /tmp/cand/test_<k>.py.`
- Cabang patch `k ∈ {a..f}`: `MODUS: TULIS PATCH (<gaya_k>). Simpan hasil hanya dengan memanggil write_file ke /tmp/cand/prop_<k>.txt.`

Parameter per cabang [A] (nilai awal usulan, bukan hasil ukuran; satu perubahan per percobaan):

| Cabang | `temperature` | Gaya | `seed` |
| :-- | :-- | :-- | :-- |
| `prop_a` | 0,20 | minimal, konservatif (cadangan utama) | tetap, berbeda |
| `prop_b` | 0,32 | minimal | tetap, berbeda |
| `prop_c` | 0,44 | defensif edge-case | tetap, berbeda |
| `prop_d` | 0,56 | defensif edge-case | tetap, berbeda |
| `prop_e` | 0,68 | ikuti konvensi penamaan modul | tetap, berbeda |
| `prop_f` | 0,80 | alternatif struktural ringkas | tetap, berbeda |
| `test_a..d` | 0,20 / 0,35 / 0,50 / 0,65 | gaya tes tetangga | tetap, berbeda |

Semua cabang: `thinking_budget: 1024`, `include_thoughts: false`, `max_output_tokens: 3072`. Bila V-27 menunjukkan payload `write_file` terpotong, naikkan `max_output_tokens` ke 4096 sebagai satu perubahan tersendiri.

**Format keluaran:** *Patch:* satu atau lebih blok `FILE: <path>`, `OLD:` (verbatim ≥3 baris dari `{localization}`), `NEW:`, lalu `ALASAN:` ≤60 kata; dilarang unified diff mentah; blok kecil agar tag tool call tidak terpotong (TC-07). *Tes:* satu berkas pytest ≤3 fungsi bergaya tes tetangga; nama API mengikuti aturan N; dilarang mengimpor nama yang tidak ada di isu atau `localization`.

**Skrip `skills/funnel/scripts/funnel.py`** (pustaka standar; argumen berdefault: `--workdir /workspace`, `--cand /tmp/cand`, `--deadline-seconds 90`). **Skrip tidak punya akses ke isu atau state ADK**; hanya ke `/tmp/cand/*` dan `/workspace`. Invarian: `deadline ≤ timeout_seconds − 30` (§5.2). Alokasi `D` = deadline: langkah 1–4 ≤ 0,4·D; langkah 5–8 sisanya. Tes yang tidak sempat dijalankan dalam jatah langkah 3–4 dilewati dan dicatat. Semua proses pytest berjalan **serial** (2 vCPU, 4 GiB).

1. **Isolasi & rekaman awal (V-26):** simpan `git status --porcelain` awal (U0); verifikasi bahwa modul target (dari `FILES`) diimpor dari `/workspace` (`PYTHONPATH=/workspace`, cetak `__file__`). Gagal: `status: abort_isolation`.
2. **Parse toleran & validasi patch.** Ekstrak `NAMES`, `TARGET_TESTS`, `NEIGHBOR_TESTS`, `FILES` dengan regex case-insensitive. Bila bagian hilang atau salah format: `FILES` ← path dari baris `FILE:` di `prop_*.txt`; `NAMES` kosong (dicatat `names_missing`) sehingga hanya aturan A dan B-sumber di langkah 3 yang berlaku; tidak ada pengambilan data dari isu. Setiap blok `prop_*.txt` valid bila: path di bawah `/workspace`; **bukan** berkas terproteksi (pola §1 "Patch", NC-08); `OLD` muncul **tepat 1 kali** di berkas; `OLD != NEW`; blok dalam satu berkas tidak tumpang tindih. `diff_lines` = jumlah baris tambah + hapus dari `difflib.unified_diff(OLD, NEW)` tanpa header; **`diff_lines == 0` gugur**. Alasan gugur dicatat (`edit_not_found`, `protected`, `noop`, `parse`).
3. **Saring tes reproduksi pada kode asli (V-28, V-29).** Per berkas satu panggilan: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/workspace pytest <file> -p no:cacheprovider -p no:anyio -o timeout=0 --tb=short --junitxml=/tmp/cand/res_<t>.xml -q`, timeout `min(25 dtk, jatah tersisa)`. Kandidat uji: `/tmp/cand/test_*.py` **dan** node `TARGET_TESTS` yang ada di repo. Tes lolos saringan hanya bila gagal (`failures>0` atau `errors>0`) dengan klasifikasi berikut, berdasarkan atribut `type`/`message` JUnit dan **frame terdalam (F)** pada traceback (`--tb=short`):
   - **A.** `AssertionError`: terima.
   - **B.** `ValueError`, `KeyError`, `IndexError`, `RuntimeError`, `TypeError`, `AttributeError`: terima bila F berada di `/workspace` dan bukan berkas tes/`conftest`. Bila F berada di berkas tes (`/tmp/cand` atau tes repo): hanya `AttributeError`/`TypeError` yang pesan galatnya menyebut nama ∈ `NAMES` yang diterima; sisanya dibuang.
   - **C.** `ImportError`/`ModuleNotFoundError`/`NameError`: terima hanya bila nama yang hilang ∈ `NAMES` dan (untuk impor) paket akarnya adalah paket repo.
   - **Dibuang:** lulus di kode asli, `SyntaxError`, `IndentationError`, `TabError`, `SystemExit`, galat collection/fixture, F di `site-packages` atau modul di luar `/workspace`, timeout, `skipped`.
4. **Penjaga regresi.** Bila `NEIGHBOR_TESTS` kosong atau tak ada di repo: cari hingga 2 berkas `tests/**/test_<stem>.py` untuk tiap berkas di `FILES`. Jalankan pada kode asli; hanya node yang **lulus** menjadi penjaga (NC-04). Bila tetap kosong: dicatat `no_guard`.
5. **Matriks Patch × Tes.** Untuk kandidat valid berurutan `a → f`: simpan byte asli → terapkan substitusi → `python3 -m py_compile` berkas tersentuh (gagal = gugur) → satu panggilan pytest atas tes tersaring + penjaga → catat `M[p][t]`, regresi `r_p`, `diff_lines` → pulihkan dari byte asli dan pastikan `git status --porcelain` sama dengan U0 (V-23). Bila `D` tercapai: berhenti, lanjut langkah 6 dengan yang sudah selesai (`prop_a` dievaluasi pertama).
6. **Seleksi konsensus CodeT.** `eligible` = valid, terkompilasi, `r_p = 0`. `S_p` = tes tersaring yang diluluskan. Kelompokkan `eligible` ber-`S_p` identik; `Score(G) = |G| × |S_G|`. Pilih `Score > 0` tertinggi; seri: `diff_lines` terkecil (> 0), lalu urutan `a..f`.
7. **Fallback deterministik bila tak ada `Score > 0`:** (1) `prop_a` bila `eligible`; (2) `eligible` pertama urut `b..f`; (3) kandidat terkompilasi dengan `r_p` terkecil dan `diff_lines > 0`; (4) `chosen: null`.
8. **Terapkan pemenang & bersihkan.** Terapkan pemenang di `/workspace`; hapus hanya path untracked (`??`) yang tidak ada di U0 (termasuk `__pycache__`/`.pytest_cache` bila muncul); **berkas tracked tidak pernah dihapus**. Cetak ringkasan ≤25 baris (pilihan, alasan, jumlah tes tersaring, matriks ringkas, `r_p`, `diff_lines`, `clean`, flag `names_missing`/`no_guard`) agar masuk jejak ATIF.

**`applier` (urutan tetap):**
1. `get_status` (gratis); baca `time_seconds_remaining`.
2. Jalankan skrip: bila sisa waktu ≥ 150 dtk gunakan perintah **tanpa argumen**; bila lebih kecil, gunakan templat dengan `--deadline-seconds 40` [A]. Sintaks pemanggilan `run_skill_script` dipastikan di V-02. Dua templat ini ditulis literal di prompt.
3. Baca ringkasan.
4. Turn tersendiri tanpa pekerjaan lain: `submit_patch`.
5. Bila `chosen: null` atau `abort_isolation`: terapkan `prop_a` (bila ada) dengan satu `edit_file`, `py_compile`, `git status --short`, lalu `submit_patch`. Bila tak ada kandidat terkompilasi dan sisa call/waktu di atas pemicu §4.3, satu usaha edit langsung dari `localization` dibolehkan; selain itu `submit_patch`. Diff kosong pasti gagal.

**Anggaran call [A]:** lokalisasi ≤6 + cabang 10 (J1) + skrip 1–2 + cadangan `edit_file`/`read_file` ≤3 ≈ ≤21; `max_tool_calls: 35` memberi margin; `get_status` dan `submit_patch` gratis. Kecukupan dan cara hitung sub-agen diukur di V-16.

**Tangga fallback (kegagalan → tindakan):**

| Gejala | Uji | Tindakan |
| :-- | :-- | :-- |
| `SequentialAgent` dipotong nudge setelah `localizer`, atau terminasi `submit_patch` bermasalah | V-15 | **Rung 1:** root `LlmAgent` memanggil `agent_tool` → `ParallelAgent`, lalu `funnel.py` |
| Jembatan J1 gagal (payload terpotong, `write_file` tidak terhitung benar, state tak terisi) | V-27 | **J2:** `applier` menyalin `{prop_*}` ke berkas, dengan N kecil (rawan salah salin) |
| `ParallelAgent` bermasalah di SDK v1.36 [K] (Rung 1 juga memakainya, jadi tidak membantu) | V-15/V-27 | **Rung 2:** satu `LlmAgent` *batch-writer* menulis 2 tes + 3 patch sekuensial ke `/tmp/cand/` dalam sesi ≤8 giliran [A], lalu `funnel.py` |
| Semua di atas gagal | | **Rung 3:** buang Varian P, kembali ke Varian 0 |

---

## 4. ATURAN TOOL & CIRCUIT BREAKER

### 4.1 Kontrak tool
- **TC-01** Read-Before-Edit. **TC-02** `get_code_neighbors` hanya setelah ada simbol bertitik dan blok graf ada di prompt. **TC-03** `edit_file` `old_string` ≥3 baris verbatim. **TC-04** satu edit, satu verifikasi. **TC-05** keluaran tes lewat `timeout N ... 2>&1 | tail -n 30`. **TC-06** gabungkan perintah; dilarang `ls`/`cat` berulang. **TC-07** payload kecil agar tag `<|tool_call>` tak terpotong `max_output_tokens`.

### 4.2 Larangan
- **NC-01** jangan ubah/hapus/skip tes asli. **NC-02** berkas sementara hanya di `/tmp` (berkas baru di `/workspace` ikut `git add -N .`). **NC-03** `read_file` ≤120 baris. **NC-04** jangan `pytest` polos atau seluruh suite; abaikan kegagalan bawaan repo. **NC-05** jangan mengarang nama yang belum terkonfirmasi lewat `read_file`/grep. **NC-06** jangan klaim "tes lulus" tanpa keluaran perintah pada giliran yang sama. **NC-07** jangan ubah signature publik; parameter baru opsional, default, di akhir. **NC-08** jangan sentuh berkas terproteksi (§1 "Patch"). **NC-09** jangan cari paket di `/usr/local/lib`, `/opt`.

### 4.3 Invarian & circuit breaker
- Setiap edit diikuti `py_compile`; gagal = pulihkan berkas.
- **Pemicu [A]:** `time_seconds_remaining ≤ max(20% batas, 1,5 × latensi turn p90)`; atau `tool_calls_remaining ≤ 2`; atau 3 siklus edit→verifikasi gagal; atau 2 panggilan identik berturut-turut.
- **Tindakan:** pilih kandidat terkompilasi terbaik (`diff_lines > 0`), bersihkan berkas baru, `submit_patch` pada turn tersendiri.
- Telemetri: `get_status` tiap 3–4 call.

---

## 5. KONFIGURASI, ANGGARAN, STRUKTUR

### 5.1 Anggaran waktu per tugas (M15)
Plafon total ≤11 jam: `H = 39600 s`; `O` = overhead setup sandbox terukur (awal ≤3600 s [A]).
- **Batas deterministik:** `N_plan = 150`; `L_safe = floor((H − O)/(N_plan × 60)) = floor(36000/9000) = 4` menit. Jaminan `N·L·60 + O ≤ H` untuk N ≤ 150 tanpa asumsi distribusi. **Submission #1: `max_time_minutes: 4`.**
- **Batas elastis (Submission #2+):** jalankan varian di dev dengan batas lebar (10 menit), ≥30 tugas; bootstrap ≥10.000 resampel `S(L) = Σ_{j=1..N} min(t*_j, 60L)`; pilih `L` bulat terbesar (`4 ≤ L ≤ 10`) dengan persentil ke-99 dari `O + S(L) ≤ H` pada **kedua** skenario: (a) N=120, waktu ×1,0; (b) N=150, waktu ×1,2 [A]. Tanpa bootstrap, pakai `L_safe`.
- **Konfirmasi:** run ekstrapolasi penuh ≤11 jam (§14). Bila `max_time_minutes` menerima pecahan (V-20), gunakan prosedur sama.
- **Alokasi contoh Varian P pada L=4 [A, harus diukur]:** 240 dtk − cadangan 20% (48) = 192 dtk; lokalisasi ≈45 + paralel ≈45 + funnel ≤90 + submit ≈10 ≈190. Margin tipis: kemungkinan P membutuhkan `L ≥ 5`; diputuskan ukuran §2.4, bukan tebakan.

### 5.2 `eval_config.yaml`
Hanya empat field ini; semantik `timeout_seconds` (per perintah atau per tugas) dan perilaku saat `max_time_minutes` habis diuji di V-06/V-20. Nilai di bawah [A], kecuali `max_turns: 50` yang sama dengan sampel.

Varian 0 (Submission #1):
```yaml
evaluation:
  timeout_seconds: 120
  max_tool_calls: 30
  max_time_minutes: 4
  max_turns: 40
```

Varian P (Funnel):
```yaml
evaluation:
  timeout_seconds: 120      # invarian: --deadline-seconds funnel.py (90) <= timeout_seconds - 30
  max_tool_calls: 35
  max_time_minutes: 4       # diperbarui via M15; P kemungkinan butuh >= 5 (lihat 5.1)
  max_turns: 50
```

### 5.3 `configs/sampling.yaml` (Varian 0)
```yaml
temperature: 0.2
max_output_tokens: 6144     # = thinking_budget + 4096
thinking_config:
  thinking_budget: 2048
  include_thoughts: false
```
`thinking_budget` ∈ {0, 1024, 2048, 4096} diukur dengan tokens/s (§2.3). Jangan pakai `thinking_level`. Satu perubahan per percobaan.

### 5.4 Struktur arsip
```text
submission_root/                         # isi di-zip; agent.yaml di ROOT zip
├── agent.yaml                           # satu-satunya root config
├── eval_config.yaml
├── configs/sampling.yaml
├── prompts/
│   ├── system.md                        # Varian 0
│   ├── localizer.md, applier.md, funnel_common.md        # Varian P
│   └── branch_test_{a..d}.md, branch_prop_{a..f}.md      # 10 berkas hasil skrip build [A]
├── sub_agents/                          # hanya Varian P; model identik dengan agent.yaml
│   ├── localizer.yaml, applier.yaml, branches.yaml       # branches = ParallelAgent
│   └── branch_test_{a..d}.yaml, branch_prop_{a..f}.yaml  # 10 LlmAgent (temperature/seed berbeda) [A, V-07/V-30]
├── skills/funnel/                       # hanya Varian P
│   ├── SKILL.md                         # frontmatter: name: funnel
│   └── scripts/funnel.py
└── adapters/                            # kosong
```
Prompt cabang dibuat oleh skrip build **di luar arsip** (tidak boleh ada `.py` di luar `skills/`): prefiks identik (`funnel_common.md` + placeholder) + dua baris penutup unik; hasilnya (`.md`) masuk arsip. Aturan: tanpa symlink; satu nama model di semua YAML (hapus YAML tak terpakai); tanpa `{...}` literal di prompt kecuali placeholder yang pasti terisi (`{problem_description}`, `{localization}`; `{prop_*}` hanya bila J2); contoh JSON di prompt ditulis tanpa kurung kurawal atau di-escape sesuai sampel resmi (V-07). Nama field kelas agen dicocokkan ke `sample_submission`, bukan ditebak. Validasi dengan compiler resmi + `package_and_validate.py` sebelum tiap submit.

### 5.5 Cadangan skrip `funnel.py`
Bila `run_skill_script` tak bisa Python atau tak bisa mengakses `/workspace` (V-02): tulis skrip ke `/tmp/funnel.py` via `write_file` (satu payload besar; ukur biayanya) lalu jalankan via `run_command`; bila tak bisa, buang Varian P. Skrip hanya pustaka standar. Konversi argumen list tunggal oleh harness hanya terjamin untuk `skill_name` dan `file_path` [V\*]; argumen lain tidak terjamin.

---

## 6. GERBANG ANTI-HALUSINASI (2 TINGKAT)
- **G1 Grounding:** setiap berkas/simbol/rentang/jangkar `OLD:` berasal dari pembacaan aktual di sesi (`localization` verbatim pada P; `read_file`/grep pada Varian 0). `OLD` tak cocok = kandidat gugur.
- **G2 Lint:** `py_compile` setelah tiap perubahan; pada P dijalankan `funnel.py` setelah tiap penerapan; gagal = kandidat tak valid.
- Disiplin prompt murah: klaim hasil menyebut perintah dan keluarannya; hipotesis dikutip dari isu/traceback.
- **Aturan dokumen (v3.4):** tiap fakta wajib berlabel; angka tanpa sumber wajib [A]; klaim tentang kemampuan skrip/harness yang belum diuji wajib masuk V-tests.

---

## 7. MODUL

| Prioritas | Modul |
| :-- | :-- |
| **P0** | Varian 0, M11, M12, M15, benchmark §2.3, V-tests hari pertama |
| **P1** | Varian P (Funnel + `funnel.py`), M13, M7 (versi prompt) |
| **P2** | M5, M8, `deep_think`, 12B+P bila lolos |
| **Dibekukan/ditutup** | Varian S (M1–M4) dibekukan; M14, M10 ditutup |

- **M7 Governor waktu (prompt):** pada 50% waktu tanpa patch terkompilasi, paksa edit hipotesis terbaik; pada pemicu §4.3 kirim. Tanpa perpanjangan anggaran.
- **M11 Harness dev:** `swegemma eval` resmi (`--timeout-seconds`, `--max-tool-calls`, `--max-time-minutes`, `--verification-timeout-seconds`) di kernel 4×L4 dengan model QAT persis; CLI bfloat16 hanya untuk uji logika. Dev set gold-check (§10.1). Keluaran JSON per tugas: lulus, waktu, call, alasan gagal, ukuran diff.
- **M12 Telemetri:** per tugas waktu per fase, jumlah call, `edit_not_found`, ukuran diff, diff kosong, berkas sampah, token thinking. Varian P tambahan: waktu tiap tahap, ringkasan `M[p][t]` dan `r_p`, jumlah tes lolos saringan, kandidat gugur (parse/OLD/noop/compile/protected), pilihan dan alasan, status isolasi, flag `names_missing`/`no_guard`. **Diagnosis offline:** kandidat dipulihkan dari jejak ATIF (blok `write_file` tiap cabang, V-27), tiap kandidat diterapkan ke salinan bersih dan diuji dengan tes gold. Definisi [A] pada tugas gold-check: `pass@1` = rata-rata lulus-gold per kandidat; `pass@6 oracle` = fraksi tugas dengan ≥1 kandidat lulus-gold; `selection_accuracy` = Σ lulus-gold(pilihan) / Σ 1[oracle].
- **M13 Aturan penamaan N** (masuk `funnel_common.md`, `localizer`, dan Varian 0 bila menang): (1) nama/parameter tertulis di isu dipakai verbatim termasuk urutan argumen; (2) bila tak tertulis, tiru pola saudara terdekat di modul yang sama; (3) jangan ganti nama API yang ada; (4) argumen baru opsional di akhir dengan default (NC-07). Ukuran: *naming-miss rate* = kegagalan gold dengan `AttributeError`, `TypeError: unexpected keyword`, atau `ImportError` pada API baru, P vs Varian 0.
- **M15 Bootstrap batas waktu:** §5.1.

---

## 8. KONTRAK PROMPT
- Agen tunggal ≤1,2k token (+ playbook ≤600). Tiap agen P ≤1k token bagian tetap; `{localization}` dinamis dihitung terpisah dan harus muat di 32k bersama thought dan keluaran. Urutan instruksi cabang mengikuti §3.3.
- Instruksi literal, berurutan, kalimat pendek. Aturan eksplisit: "lokalisasi ≤6 call, edit sebelum call ke-12, tes terarah saja, berkas sementara di /tmp, `submit_patch` terakhir".
- Playbook statis (≤600 token): pola bug Python umum (None/kosong, off-by-one, default mutabel, encoding, zona waktu, regex, urutan dict/set), kebiasaan pytest/tox, "ubah seminimal mungkin".
- Dilarang asumsi nama paket/struktur folder/konvensi pustaka tertentu (repo-agnostic).

---

## 9. METRIK & AMBANG

| Metrik | Ambang |
| :-- | :-- |
| Grounding failure | ≤5% |
| Edit-not-found | ≤8% |
| Phantom API | ≤3% |
| Junk-file | 0% |
| Empty-patch | ≤5% |
| Over-budget (lewat `max_time_minutes` atau `max_tool_calls`) | ≤5% |
| Regresi tes lama (P2P lulus awal jadi gagal) | tidak naik vs Varian 0 |
| Naming-miss | turun pada P vs Varian 0 [A] |
| Varian P | parse ≥90%; keragaman diff ≥2 pada ≥60% tugas; ≥1 tes lolos saringan dilaporkan; `pass@6/pass@1 ≥ 1,4`; `selection_accuracy ≥ 0,4`; waktu sesuai §2.4 |

**Fixture adversarial (≥7 dari 8 lulus):** isu menyebut fungsi tak ada; dua simbol sama nama; traceback di luar repo; isu tanpa traceback; tes asli gagal sebelum patch; patch memicu `ImportError`; instruksi di isu menyuruh mengubah tes; repo tanpa pytest. Lulus bila agen tak mengarang dan berakhir dengan diff bersih atau berhenti dengan benar.

---

## 10. PROTOKOL EKSPERIMEN

### 10.1 Dev set gold-check
Dari 129 tugas publik: terapkan patch referensi lalu `test_patch` pada snapshot bersih, jalankan perintah verifikasi resmi (§1) 2×. Simpan hanya tugas dengan gold lulus 2/2, `FAIL_TO_PASS` gagal di kode asli, tanpa node `skipped`, tanpa kebutuhan jaringan. Ambil dev M ≥ 24 (target 30–40) seimbang antar-repo + 10 tugas hold-out (tidak dipakai tuning). Nama field patch referensi di `tasks.jsonl` dicek di V-10. **Peringatan:** repo publik terkenal, model mungkin menghafal; skor absolut dev terlalu optimistis, hanya selisih berpasangan dipercaya.

### 10.2 Multi-run berpasangan
Tiap lengan **R = 3** (R = 4 bila perbatasan), seed bervariasi, konfigurasi vLLM sama, urutan lengan diacak antar-run [K: berkas identik pernah bernilai 7–13 dari 58 tugas]. `p_i` = fraksi lulus tugas i; `Δ̂ = rata-rata_i(p_i^baru − p_i^lama)`; `LB80` = persentil ke-20 bootstrap berpasangan (10.000 resampel).

### 10.3 Aturan keputusan
| Tier | Untuk | Terima bila |
| :-- | :-- | :-- |
| **C** | menambah kompleksitas/waktu/ganti model (Varian P, 12B vs 31B, thinking lebih besar) | `Δ̂ ≥ +0,03` **dan** `LB80 > 0` **dan** semua pagar lolos |
| **S** | perubahan prompt tanpa biaya | `Δ̂ ≥ 0` dan semua pagar lolos |

Pagar: ekstrapolasi ≤11 jam; empty-patch tak naik >3 poin persentase; over-budget ≤5%; regresi tes lama tak naik; metrik §9 di bawah ambang. **Inkonklusif** (`Δ̂ > 0`, `LB80 ≤ 0`) = tolak. Ambang +0,03, 80%, dan R adalah pilihan kebijakan [A]; dengan M≈30, `LB80 > 0` biasanya menuntut `Δ̂ ≈ +0,05` [A].

### 10.4 Saringan & anggaran komputasi
Urutan P: gerbang §2.4 (diagnosis offline) → saringan R=1 (buang bila `Δ̂ < −0,05` atau V-test terkait gagal) → konfirmasi R=3 hanya untuk yang lolos. Perkiraan 30 tugas × 3 run × ~3 menit ≈ 4,5 jam GPU per lengan [A]; rencanakan 4–5 lengan konfirmasi; periksa kuota GPU sebelum mulai. Satu perubahan per lengan; catat hash zip, konfigurasi, hasil. Tanpa tuning mikro pada dev.

### 10.5 Peran leaderboard & submission
Leaderboard publik (58 tugas) hanya sanity check; **keputusan tidak boleh berdasar satu skor leaderboard.** Jatah ≈15 submission [A]: #1 Varian 0; #2 Varian 0 + `L`; #3–#10 kandidat lolos uji lokal; sisanya final dan cadangan antrean. Tanpa eksperimen baru pada H-3.

---

## 11. JADWAL (WIB)

Hari ini Rabu 18 Nov 2026; batas hari kiriman diasumsikan UTC [K] (00:09 WIB = 17:09 UTC hari sebelumnya; V-31).

| Fase & rentang | Fokus | Gerbang |
| :-- | :-- | :-- |
| **F0** 18 Nov | Inspeksi `HARNESS_README.md`, `sample_submission`, `tasks.jsonl` (V-01, V-06, V-07, V-10, V-12) dan status [U]; susun & validasi Varian 0; kirim **S1** (`max_time_minutes: 4`) | **G0:** compiler resmi lulus dan S1 antre sebelum Kam 19 Nov 06:59 WIB |
| **F1** 18–20 Nov | Gold-check M11 (M ≥ 30 + 10 hold-out); benchmark §2.3; run dev lebar + bootstrap M15; **S2** (Varian 0 + `L`); **V-31 diuji dengan perilaku antrean S1/S2** | **G1:** waktu antrean nyata terukur, `L` terkunci, keputusan 12B |
| **F2** 19–22 Nov | V-15..V-17, V-25..V-30; tulis & unit-test `funnel.py`; diagnosis M12 pada E4B (P=6) | **G2 (GO/NO-GO):** §2.4 |
| **F3** 23–25 Nov | Saringan R=1 lalu konfirmasi R=3; **S3**; verifikasi ulang status `Joined` sebelum 26 Nov 06:59 WIB | **G3:** pemenang memenuhi Tier-C/Tier-S |
| **F4** pembekuan | Lihat skenario di bawah | **G4:** kandidat final masuk antrean sesuai skenario |
| **F5** 30 Nov–2 Des | Pantau antrean (hanya hotfix format bila ditolak); pilih tepat 2 submission final di Kaggle sebelum **Kam 3 Des 06:59 WIB** | **G5:** 14 kriteria §14 terpenuhi |

**Skenario F4 (diputuskan oleh V-31; semua turunan angka 81 jam [K]):**
- **Skenario A (≥2 submission boleh pending):** bekukan kode Kam 26 Nov; kirim S4 (Final A) dan S5 (Final B) pada hari berbeda (1/hari [K]); **S5 paling lambat Min 29 Nov 18:00 WIB**: 18:00 + 81 jam = Kam 3 Des 03:00 WIB < 06:59 WIB.
- **Skenario B (1 pending, serial):** dua kiriman final baru tidak muat. Batas kirim S4 = 29 Nov 18:00 − 81 jam = **Kam 26 Nov 09:00 WIB**, sehingga kode Final A dibekukan **Rabu 25 Nov**. **Final B diambil dari submission yang sudah bernilai (mis. S3 bila E4B)**; hanya satu kiriman final baru.
- Pada kedua skenario, 2 final dipilih dari submission yang sudah selesai dinilai; submission tertahan antrean bukan kandidat final yang aman.

---

## 12. DAFTAR VERIFIKASI ([V\*]/[K]/[A]/[U] → lulus)

| # | Pertanyaan | Jika gagal | P |
| :-- | :-- | :-- | :-- |
| V-01 | ROLE.md cocok dengan `HARNESS_README.md` asli (nama tool, skema argumen, tanggal batas)? | Perbarui dokumen; hapus `*` per baris | P0 |
| V-02 | `run_skill_script` bisa Python, baca/tulis `/workspace`, dan bagaimana sintaks argumennya? | §5.5; bila gagal, buang P | P0 |
| V-03 | Overhead per skrip; dihitung sebagai tool call? | §5.5; bila mahal, buang P | P0 |
| V-05 | Auto-compaction (tiap 15 event) tidak merusak `{localization}`/state cabang | Ringkas prompt | P1 |
| V-06 | Compiler menerima 4 field `eval_config`; semantik `timeout_seconds` | Sesuaikan §5.2 | P0 |
| V-07 | Sintaks `agent.yaml` untuk `SequentialAgent`, `ParallelAgent`, `output_key`, `agent_tool`, `!include`, escape kurung kurawal | Ganti sintaks | P0 |
| V-08 | `submit_patch` memakai `git diff` terhadap `_swegemma_baseline` | – | [V\*] |
| V-10 | Struktur `tasks.jsonl`, nama field patch referensi dan `test_patch` | Hitung ulang dev | P0 |
| V-11 | Ukuran set publik | – | P0 |
| V-12 | Ekstensi sah | Hapus berkas | P0 |
| V-14 | Tokens/s 31B, 12B, E4B | Sesuaikan thinking dan N | P0 |
| V-15 | Root `SequentialAgent` + terminasi `submit_patch` + nudge | Rung 1 (§3.3) | P0 |
| V-16 | Call dan giliran sub-agen memotong `max_tool_calls`/`max_turns`? | Hitung ulang / buang | P0 |
| V-17 | Konteks sub-agen terpisah; `{localization}` terisi; `include_contents: none` tetap benar saat cabang membawa `write_file` | Buang P | P0 |
| V-18 | Throughput agregat dan KV konkurensi 1/3/4 | Buang P | P0 |
| V-19 | Harness menjalankan tugas serial atau paralel? | Paralel: buang P | P0 |
| V-20 | `max_time_minutes` bulat atau pecahan; diff dipungut saat habis? | Sesuaikan §5.1, §4.3 | P0 |
| V-21 | Tes di `/tmp/cand/` memakai konfigurasi/fixture repo? Opsi diuji: `-c /workspace/pytest.ini --rootdir /workspace`; memuat `conftest` repo sebagai plugin (`-p conftest` dengan `PYTHONPATH=/workspace`) [A] | Letakkan tes di lokasi lain, bukan `/workspace` | P0 |
| V-23 | Pemulihan dari byte asli mengembalikan `git status`/`git diff` ke keadaan awal | `git stash` atau salinan | P1 |
| V-24 | 12B berjalan dengan `hf-overrides` | Buang 12B | P0 |
| V-25 | Prefix cache vLLM aktif dan terpakai pada 10 cabang; urutan template (skema tool → instruksi → konten) menghasilkan prefiks sama | Gerbang KV tanpa berbagi; kurangi N atau buang | P0 |
| V-26 | Tes di `/workspace` mengimpor kode `/workspace` (bukan salinan terpasang) | `PYTHONPATH=/workspace`; bila gagal, buang | P0 |
| V-27 | J1: `write_file` per cabang bekerja, payload tak terpotong, call terhitung benar, kandidat bisa dipulihkan dari ATIF | J2, lalu Rung 2, lalu buang | P0 |
| V-28 | Tak ada `__pycache__`/`.pytest_cache` ikut diff | Perketat pembersihan; bila bocor, buang | P0 |
| V-29 | JUnit XML + `--tb=short` cukup untuk memperoleh `type`, `message`, dan frame terdalam (F) untuk klasifikasi §3.3 langkah 3 | Perbaiki parser; bila tak mungkin, batasi ke aturan A | P0 |
| V-30 | Sintaks dan batas 10 `sub_agents` per `ParallelAgent`; prompt cabang hasil build membagi prefiks identik | Rung 2 | P0 |
| V-31 | Aturan antrean: boleh ≥2 pending? kapan reset harian (UTC?)? durasi antrean S1/S2 | Pilih Skenario B (§11) | P0 |

V-04, V-09, V-13, V-22 dipensiunkan (digantikan V-17, dihapus, M10 ditutup, M14 ditutup).

---

## 13. REGISTER RISIKO

| Risiko | Dampak | Mitigasi |
| :-- | :-- | :-- |
| Lewat 12 jam | Skor 0 | §5.1: `L_safe`, bootstrap 99%, ekstrapolasi ≤11 jam |
| Nudge/terminasi memotong P (V-15) | Pipeline putus | Rung 1; buang P |
| Konkurensi memakan headroom; KV rebutan | P tak lebih cepat | Gerbang §2.3; E4B/12B saja |
| Prefiks tak terbagi (V-25) | Cabang antre, waktu > `L` | Kurangi N; buang |
| Proposal terpotong atau OLD tak cocok | Kandidat gugur | Blok kecil, verbatim, pantau `edit_not_found` |
| Tes model salah/sirkular | Konsensus condong ke patch salah | Saringan klasifikasi §3.3; `selection_accuracy ≥ 0,4` |
| `funnel.py` bug / melewati `timeout_seconds` | Skor 0 / patch hilang | Varian 0 sebagai #1; deadline < timeout − 30; unit-test; V-02/V-03 |
| Pemulihan workspace salah | Diff hilang/bocor | Pulih dari byte asli; V-23; simpan `/tmp/cand_k.patch` |
| Isolasi palsu | Seleksi acak | V-26; abort isolasi → cadangan `prop_a` |
| `ParallelAgent` bermasalah [K] | Pipeline putus | Tangga §3.3 |
| `__pycache__`/cache ikut patch | Diff kotor | V-28; `PYTHONDONTWRITEBYTECODE=1`; hapus hanya `??` baru |
| Hasil dev tak menggeneralisasi | LB privat turun | Selisih berpasangan, hold-out, R≥3 |
| Antrean 48–81 jam; aturan pending | Kehilangan kandidat final | Kirim awal; V-31; Skenario B; final dari submission bernilai |
| Kuota GPU habis | Tak bisa uji | Saringan R=1, subset kecil |
| Pelanggaran data/berbagi | Diskualifikasi | Tak commit data; tak berbagi privat |
| Model berbeda antar YAML | Zip ditolak | Compiler resmi + `package_and_validate.py` |
| Klaim [U]/[K] ternyata salah | Rencana meleset | F0 dan V-01 memverifikasi ulang |

---

## 14. KRITERIA PENERIMAAN (100% SELESAI)
1. Root config tunggal di root `.zip`, lolos compiler resmi, satu string model di semua YAML, hanya 4 field `evaluation:`.
2. Arsip `< 3 GiB`, ekstensi sah, tanpa symlink, dibuat ke `/kaggle/working/submission.zip`.
3. Diff bersih pada ≥10 tugas dev: 0 berkas sampah, 0 perubahan berkas terproteksi.
4. Bootstrap p99 `O + S(L) ≤ 39600 s` pada skenario (a) dan (b), dan ekstrapolasi penuh ≤11 jam.
5. Seluruh metrik §9 di bawah ambang pada run konfirmasi.
6. ≥7 dari 8 fixture adversarial lulus.
7. Setiap komponen di luar Varian 0 lolos §10 (Tier-C/S); Varian P juga lolos §2.4.
8. Final B memakai `e4b` (atau `e2b`) dan terpilih sebagai satu dari 2 final.
9. Submission #1 = Varian 0 murni, tanpa skrip/sub-agen, `max_time_minutes ≤ 4`.
10. Varian P: matriks `Patch × Test` dan alasan pilihan tercatat per tugas di ATIF; diff akhir dari `funnel.py` atau cadangan tercatat; 0 berkas sampah.
11. V-01 lulus dan semua tanda `*` pada fakta yang dipakai telah dihapus; status [U] terverifikasi.
12. V-31 terjawab dan skenario F4 (A atau B) terkunci.
13. Tidak ada klaim [K]/[A] yang dipakai sebagai dasar keputusan tanpa V-test lulus.
14. Final A dan Final B adalah submission yang sudah selesai dinilai pada saat pemilihan.

---

## Lampiran A. Pemetaan 8 Keputusan Arsitektural (ROLE.md §10)

| # | Keputusan | Nilai terkunci v3.4 |
| :-- | :-- | :-- |
| 1 | Model & track | Tanpa LoRA. S1: E4B atau model terbesar yang lolos §2.3. Final B: E4B. 12B/31B bersyarat |
| 2 | Topologi | Varian 0: satu `LlmAgent`. Varian P: `SequentialAgent` + `ParallelAgent` (`include_contents: "none"`, `output_key`) |
| 3 | Retensi konteks | `include_thoughts: false`, `thinking_budget > 0` (§5.3; cabang P: 1024) |
| 4 | Skills vs built-in | Varian 0: tanpa skill. P: hanya `skills/funnel` (V-02/V-03) |
| 5 | Lokalisasi hybrid | Peta Turn-0 + `search_similar_code`/`get_code_neighbors` hanya bila blok graf ada; fallback grep terarah |
| 6 | `eval_config.yaml` | §5.2 |
| 7 | Sampling | §5.3 dan tabel cabang §3.3 |
| 8 | Validasi lokal | §10 dan §7 (M11, M12) |

## Sumber
- Kaggle: Overview/Rules, forum (kaggle.com/competitions/gemma-4-developer-agent), dicocokkan di V-01.
- ROLE.md v2.0 (kutipan `HARNESS_README.md`); MASTER PRD v3.2 dan v3.3.
- ROADMAP v3.2: tidak tersedia di sesi penyusunan; klaim jadwalnya [K].
- Repo/laporan peserta [K] (daftar di v3.2 "Sumber"); ide Agentless, CodeT, CodeMonkeys dari ingatan penulis ide, belum diverifikasi [A].