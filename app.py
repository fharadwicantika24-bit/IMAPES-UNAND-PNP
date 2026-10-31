import base64
import html
import os
import uuid
from urllib.parse import quote

import streamlit as st

# ============================ KONFIGURASI ============================
st.set_page_config(page_title="HIMA Nusantara", page_icon="🏛️", layout="wide")

try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except Exception:
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

DIVISI = ["BPH", "PSDM", "Humas", "Kominfo"]
STATUS = ["Akan Datang", "Berlangsung", "Selesai"]
STATUS_WARNA = {"Akan Datang": "#2563EB", "Berlangsung": "#F59E0B", "Selesai": "#16A34A"}
JABATAN = ["Ketua Umum", "Wakil Ketua", "Sekretaris", "Bendahara", "Kadiv"]
MENU = ["🏠 Beranda", "📋 Program Kerja", "👥 Pengurus", "📞 Hubungi Kami", "🔐 Login / Dashboard Admin"]

# ============================ CSS ============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }
.stApp { background: #F8FAFC; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1200px; }
h1, h2, h3, h4 { color: #0A192F !important; font-weight: 700 !important; }
[data-testid="stSidebar"] { background: #0A192F; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span,
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #E2E8F0 !important; }
.hero { background: linear-gradient(135deg, #0A192F 0%, #1E3A5F 100%); color: #fff; padding: 3rem 2.5rem;
        border-radius: 16px; margin-bottom: 1.2rem; box-shadow: 0 10px 30px rgba(10,25,47,.25); }
.hero h1 { color: #fff !important; font-size: 2.4rem; margin: 0 0 .4rem 0; }
.hero .tag { color: #93C5FD; font-weight: 600; font-size: 1.1rem; margin-bottom: .8rem; }
.hero p { color: #CBD5E1; max-width: 720px; line-height: 1.7; }
.card { background: #fff; border: 1px solid #E2E8F0; border-radius: 14px; padding: 1.2rem 1.3rem;
        box-shadow: 0 2px 8px rgba(15,23,42,.05); margin-bottom: .8rem; }
.metric { text-align: center; border-top: 4px solid #0A192F; }
.metric .num { font-size: 2rem; font-weight: 800; color: #0A192F; }
.metric .lbl { color: #64748B; font-size: .85rem; text-transform: uppercase; letter-spacing: .05em; }
.proker { padding: 0; overflow: hidden; }
.proker img { width: 100%; height: 160px; object-fit: cover; }
.proker .body { padding: 1rem 1.2rem 1.1rem 1.2rem; }
.proker h4 { margin: .5rem 0 .3rem 0; font-size: 1.05rem; }
.proker p { color: #475569; font-size: .88rem; line-height: 1.55; margin: .2rem 0; }
.meta { color: #64748B; font-size: .8rem; margin: .15rem 0; }
.badge { display: inline-block; padding: .2rem .65rem; border-radius: 999px; font-size: .72rem;
         font-weight: 600; color: #fff; margin-right: .3rem; }
.badge-navy { background: #0A192F; }
.bar { background: #E2E8F0; border-radius: 999px; height: 8px; margin-top: .5rem; overflow: hidden; }
.bar > div { background: linear-gradient(90deg, #0A192F, #3B82F6); height: 100%; }
.person { text-align: center; }
.person img { width: 110px; height: 110px; border-radius: 50%; object-fit: cover; border: 4px solid #E2E8F0; }
.person h4 { margin: .6rem 0 .3rem 0; font-size: 1rem; }
.person p { color: #64748B; font-size: .82rem; font-style: italic; margin-top: .5rem; }
.news { border-left: 4px solid #0A192F; }
.news small { color: #64748B; }
.section-title { border-left: 5px solid #0A192F; padding-left: .7rem; margin: 1.6rem 0 .8rem 0; }
div.stButton > button, div[data-testid="stFormSubmitButton"] > button { border-radius: 8px; font-weight: 600; }
footer { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# ============================ HELPER ============================
def uid():
    return uuid.uuid4().hex[:8]


def esc(x):
    return html.escape(str(x))


def to_data_uri(f):
    return f"data:{f.type};base64,{base64.b64encode(f.getvalue()).decode()}"


def avatar(nama):
    return f"https://ui-avatars.com/api/?name={quote(nama)}&background=0A192F&color=fff&size=256"


def section(title):
    st.markdown(f"<h3 class='section-title'>{title}</h3>", unsafe_allow_html=True)


def badge(text, color):
    return f"<span class='badge' style='background:{color}'>{esc(text)}</span>"


# ============================ DATA AWAL ============================
def init_state():
    if "init" in st.session_state:
        return
    st.session_state.admin = False
    st.session_state.org = {
        "nama": "HIMA Nusantara",
        "tagline": "Berkarya, Berkolaborasi, Berdampak",
        "deskripsi": "Himpunan Mahasiswa Nusantara adalah wadah aspirasi, pengembangan diri, dan pengabdian "
                     "mahasiswa untuk menciptakan perubahan positif bagi kampus dan masyarakat.",
        "visi": "Menjadi organisasi mahasiswa yang unggul, inklusif, dan berintegritas dalam membangun "
                "generasi pemimpin masa depan.",
        "misi": ["Mengembangkan potensi dan kepemimpinan anggota",
                 "Menyelenggarakan program kerja yang inovatif dan berdampak",
                 "Membangun kemitraan strategis dengan berbagai pihak",
                 "Menjaga transparansi dan akuntabilitas organisasi"],
        "mitra": 12,
        "alamat": "Gedung Student Center Lt. 2, Kampus Nusantara, Bandung, Jawa Barat",
        "email": "info@himanusantara.ac.id",
        "wa": "6281234567890",
        "instagram": "https://instagram.com/himanusantara",
        "linkedin": "https://linkedin.com/company/himanusantara",
    }
    st.session_state.programs = [
        {"id": uid(), "nama": "Leadership Camp 2026", "divisi": "PSDM", "status": "Selesai",
         "deskripsi": "Pelatihan kepemimpinan intensif bagi seluruh anggota baru.",
         "jadwal": "12-14 Agustus 2026", "lokasi": "Lembang, Bandung", "pic": "Rina (0812-1111-2222)",
         "progress": 100, "gambar": "https://picsum.photos/seed/camp/600/300",
         "detail": "Dokumentasi: 120 peserta, 15 mentor. Materi: public speaking, manajemen konflik, dan project planning."},
        {"id": uid(), "nama": "Seminar Nasional Teknologi", "divisi": "Kominfo", "status": "Berlangsung",
         "deskripsi": "Seminar bersama praktisi industri tentang tren AI dan transformasi digital.",
         "jadwal": "Nov 2026", "lokasi": "Aula Utama Kampus", "pic": "Dimas (0813-3333-4444)",
         "progress": 65, "gambar": "https://picsum.photos/seed/seminar/600/300",
         "detail": "Alur pendaftaran: 1) Isi formulir online, 2) Konfirmasi via email, 3) Tunjukkan e-tiket saat registrasi ulang."},
        {"id": uid(), "nama": "Bakti Sosial Desa Binaan", "divisi": "Humas", "status": "Akan Datang",
         "deskripsi": "Kegiatan pengabdian masyarakat berupa edukasi dan bantuan sarana belajar.",
         "jadwal": "Des 2026", "lokasi": "Desa Cibodas", "pic": "Sari (0814-5555-6666)",
         "progress": 20, "gambar": "https://picsum.photos/seed/baksos/600/300",
         "detail": "Pendaftaran relawan dibuka melalui Sekretariat. Kuota 40 orang."},
        {"id": uid(), "nama": "Rapat Kerja & Evaluasi", "divisi": "BPH", "status": "Akan Datang",
         "deskripsi": "Evaluasi kinerja semester dan penyusunan strategi periode berikutnya.",
         "jadwal": "Jan 2027", "lokasi": "Ruang Sidang Senat", "pic": "Ketua Umum",
         "progress": 10, "gambar": "https://picsum.photos/seed/raker/600/300",
         "detail": "Dihadiri seluruh pengurus inti dan kepala divisi."},
    ]
    st.session_state.members = [
        {"id": uid(), "nama": "Andi Pratama", "jabatan": "Ketua Umum", "divisi": "BPH",
         "kutipan": "Memimpin dengan teladan dan integritas.", "foto": ""},
        {"id": uid(), "nama": "Rina Maharani", "jabatan": "Sekretaris", "divisi": "BPH",
         "kutipan": "Administrasi rapi, organisasi solid.", "foto": ""},
        {"id": uid(), "nama": "Budi Santoso", "jabatan": "Bendahara", "divisi": "BPH",
         "kutipan": "Transparansi keuangan adalah amanah.", "foto": ""},
        {"id": uid(), "nama": "Dimas Aditya", "jabatan": "Kadiv", "divisi": "Kominfo",
         "kutipan": "Menyebarkan informasi yang akurat dan menarik.", "foto": ""},
        {"id": uid(), "nama": "Sari Wulandari", "jabatan": "Kadiv", "divisi": "Humas",
         "kutipan": "Relasi baik adalah kunci kolaborasi.", "foto": ""},
        {"id": uid(), "nama": "Fajar Nugroho", "jabatan": "Kadiv", "divisi": "PSDM",
         "kutipan": "Anggota berkembang, organisasi berkembang.", "foto": ""},
    ]
    st.session_state.news = [
        {"id": uid(), "judul": "Pendaftaran Seminar Nasional Dibuka", "tanggal": "28 Okt 2026",
         "isi": "Pendaftaran peserta Seminar Nasional Teknologi kini dibuka hingga 10 November 2026."},
        {"id": uid(), "judul": "Open Recruitment Relawan Bakti Sosial", "tanggal": "20 Okt 2026",
         "isi": "Terbuka untuk seluruh mahasiswa. Daftarkan diri melalui Sekretariat."},
    ]
    st.session_state.messages = []
    st.session_state.init = True


init_state()
S = st.session_state

# ============================ SIDEBAR ============================
with st.sidebar:
    st.markdown(f"## 🏛️ {esc(S.org['nama'])}")
    st.caption("Portal Resmi Organisasi")
    page = st.radio("Navigasi", MENU, key="nav", label_visibility="collapsed")
    st.divider()
    if S.admin:
        st.success("Mode Admin aktif")
        if st.button("Logout", use_container_width=True):
            S.admin = False
            st.rerun()
    else:
        st.caption("Mode: Publik (Read-Only)")


# ============================ KOMPONEN TAMPILAN ============================
def render_proker_card(p):
    warna = STATUS_WARNA.get(p["status"], "#64748B")
    st.markdown(
        f"""<div class='card proker'>
        <img src="{esc(p['gambar'])}" alt="banner">
        <div class='body'>
            {badge(p['status'], warna)}{badge(p['divisi'], '#0A192F')}
            <h4>{esc(p['nama'])}</h4>
            <p>{esc(p['deskripsi'])}</p>
            <div class='meta'>📅 {esc(p['jadwal'])}</div>
            <div class='meta'>📍 {esc(p['lokasi'])}</div>
            <div class='meta'>👤 PIC: {esc(p['pic'])}</div>
            <div class='meta' style='margin-top:.5rem'>Ketercapaian: <b>{p['progress']}%</b></div>
            <div class='bar'><div style='width:{p['progress']}%'></div></div>
        </div></div>""",
        unsafe_allow_html=True,
    )
    with st.expander("🔎 Detail Kegiatan"):
        st.write(p["detail"] or "Belum ada rincian.")


def render_member_card(m):
    foto = m["foto"] or avatar(m["nama"])
    label = m["jabatan"] if m["jabatan"] != "Kadiv" else f"Kadiv {m['divisi']}"
    st.markdown(
        f"""<div class='card person'><img src="{esc(foto)}" alt="foto">
        <h4>{esc(m['nama'])}</h4>
        {badge(label, '#0A192F')}
        <p>“{esc(m['kutipan'])}”</p></div>""",
        unsafe_allow_html=True,
    )


def member_rank(m):
    return JABATAN.index(m["jabatan"]) if m["jabatan"] in JABATAN else 99


# ============================ HALAMAN: BERANDA ============================
def page_home():
    o = S.org
    st.markdown(
        f"<div class='hero'><div class='tag'>{esc(o['tagline'])}</div><h1>{esc(o['nama'])}</h1>"
        f"<p>{esc(o['deskripsi'])}</p></div>",
        unsafe_allow_html=True,
    )
    st.button("🚀 Lihat Program Kerja", type="primary",
              on_click=lambda: S.update(nav=MENU[1]))

    progs = S.programs
    capaian = round(sum(p["progress"] for p in progs) / len(progs)) if progs else 0
    stats = [(len(progs), "Total Program Kerja"), (len(S.members), "Anggota / Pengurus"),
             (o["mitra"], "Mitra Kerja Sama"), (f"{capaian}%", "Capaian Tahun Ini")]
    section("Ringkasan Organisasi")
    for col, (num, lbl) in zip(st.columns(4), stats):
        col.markdown(f"<div class='card metric'><div class='num'>{num}</div><div class='lbl'>{lbl}</div></div>",
                     unsafe_allow_html=True)

    section("Visi & Misi")
    c1, c2 = st.columns(2)
    c1.markdown(f"<div class='card'><h4>🎯 Visi</h4><p style='color:#475569;line-height:1.7'>{esc(o['visi'])}</p></div>",
                unsafe_allow_html=True)
    misi = "".join(f"<li style='margin-bottom:.4rem'>{esc(m)}</li>" for m in o["misi"])
    c2.markdown(f"<div class='card'><h4>🧭 Misi</h4><ol style='color:#475569;line-height:1.6;padding-left:1.1rem'>{misi}</ol></div>",
                unsafe_allow_html=True)

    section("Pengumuman & Berita Terbaru")
    if not S.news:
        st.info("Belum ada pengumuman.")
    for col, n in zip(st.columns(max(len(S.news), 1)), S.news):
        col.markdown(f"<div class='card news'><small>🗓️ {esc(n['tanggal'])}</small><h4>{esc(n['judul'])}</h4>"
                     f"<p style='color:#475569;font-size:.9rem'>{esc(n['isi'])}</p></div>", unsafe_allow_html=True)


# ============================ HALAMAN: PROGRAM KERJA ============================
def page_programs():
    st.title("📋 Katalog Program Kerja & Kegiatan")
    c1, c2, c3 = st.columns([2, 1.3, 1.3])
    q = c1.text_input("🔍 Cari kegiatan", placeholder="Ketik nama atau deskripsi...")
    fd = c2.multiselect("Divisi", DIVISI)
    fs = c3.multiselect("Status", STATUS)
    hasil = [p for p in S.programs
             if (not fd or p["divisi"] in fd) and (not fs or p["status"] in fs)
             and q.lower() in (p["nama"] + " " + p["deskripsi"]).lower()]
    st.caption(f"Menampilkan {len(hasil)} dari {len(S.programs)} kegiatan")
    if not hasil:
        st.warning("Tidak ada kegiatan yang sesuai filter.")
    for i in range(0, len(hasil), 3):
        for col, p in zip(st.columns(3), hasil[i:i + 3]):
            with col:
                render_proker_card(p)


# ============================ HALAMAN: PENGURUS ============================
def page_members():
    st.title("👥 Profil & Struktur Pengurus")
    st.caption("Susunan pengurus periode berjalan")
    ms = sorted(S.members, key=member_rank)
    inti = [m for m in ms if m["jabatan"] != "Kadiv"]
    kadiv = [m for m in ms if m["jabatan"] == "Kadiv"]
    for judul, grup in (("Badan Pengurus Harian", inti), ("Kepala Divisi", kadiv)):
        if grup:
            section(judul)
            for i in range(0, len(grup), 4):
                for col, m in zip(st.columns(4), grup[i:i + 4]):
                    with col:
                        render_member_card(m)


# ============================ HALAMAN: KONTAK ============================
def page_contact():
    o = S.org
    st.title("📞 Hubungi Kami & Transparansi")
    c1, c2 = st.columns(2)
    with c1:
        section("Informasi Kontak Resmi")
        st.markdown(
            f"""<div class='card'>
            <p>📍 <b>Sekretariat</b><br>{esc(o['alamat'])}</p>
            <p>✉️ <b>Email</b><br><a href="mailto:{esc(o['email'])}">{esc(o['email'])}</a></p>
            <p>💬 <b>WhatsApp Fast Response</b><br><a href="https://wa.me/{esc(o['wa'])}" target="_blank">+{esc(o['wa'])}</a></p>
            <p>🌐 <b>Media Sosial</b><br>
            <a href="{esc(o['instagram'])}" target="_blank">Instagram</a> &nbsp;•&nbsp;
            <a href="{esc(o['linkedin'])}" target="_blank">LinkedIn</a></p></div>""",
            unsafe_allow_html=True,
        )
    with c2:
        section("Kirim Pesan / Aspirasi")
        with st.form("form_pesan", clear_on_submit=True):
            nama = st.text_input("Nama")
            email = st.text_input("Email")
            pesan = st.text_area("Pesan, saran, atau pertanyaan", height=140)
            if st.form_submit_button("Kirim Pesan", type="primary"):
                if nama.strip() and pesan.strip():
                    S.messages.append({"id": uid(), "nama": nama, "email": email, "pesan": pesan})
                    st.success("Terima kasih! Pesan Anda telah kami terima.")
                else:
                    st.error("Nama dan pesan wajib diisi.")


# ============================ HALAMAN: ADMIN ============================
def admin_login():
    st.title("🔐 Login Admin")
    st.caption("Area khusus pengurus organisasi.")
    _, mid, _ = st.columns([1, 1.5, 1])
    with mid, st.form("login"):
        pw = st.text_input("Password Admin", type="password")
        if st.form_submit_button("Masuk", type="primary", use_container_width=True):
            if pw == ADMIN_PASSWORD:
                S.admin = True
                st.rerun()
            else:
                st.error("Password salah.")
        st.caption("Password default: admin123 (ubah via env ADMIN_PASSWORD atau st.secrets)")


def prog_fields(d, k):
    c1, c2 = st.columns(2)
    nama = c1.text_input("Nama Kegiatan", d.get("nama", ""), key=f"n{k}")
    divisi = c2.selectbox("Divisi", DIVISI, DIVISI.index(d["divisi"]) if d.get("divisi") in DIVISI else 0, key=f"d{k}")
    status = c1.selectbox("Status", STATUS, STATUS.index(d["status"]) if d.get("status") in STATUS else 0, key=f"s{k}")
    progress = c2.slider("Progress (%)", 0, 100, d.get("progress", 0), key=f"p{k}")
    jadwal = c1.text_input("Jadwal", d.get("jadwal", ""), key=f"j{k}")
    lokasi = c2.text_input("Lokasi", d.get("lokasi", ""), key=f"l{k}")
    pic = c1.text_input("PIC / Narahubung", d.get("pic", ""), key=f"c{k}")
    gambar = c2.text_input("URL Banner (kosongkan jika upload)", d.get("gambar", ""), key=f"g{k}")
    up = st.file_uploader("Atau upload banner", type=["png", "jpg", "jpeg"], key=f"u{k}")
    desk = st.text_area("Deskripsi", d.get("deskripsi", ""), key=f"x{k}")
    detail = st.text_area("Detail (alur pendaftaran / dokumentasi)", d.get("detail", ""), key=f"t{k}")
    img = to_data_uri(up) if up else (gambar or "https://picsum.photos/seed/default/600/300")
    return {"nama": nama, "divisi": divisi, "status": status, "progress": progress, "jadwal": jadwal,
            "lokasi": lokasi, "pic": pic, "gambar": img, "deskripsi": desk, "detail": detail}


def member_fields(d, k):
    c1, c2 = st.columns(2)
    nama = c1.text_input("Nama", d.get("nama", ""), key=f"mn{k}")
    jab = c2.selectbox("Jabatan", JABATAN, JABATAN.index(d["jabatan"]) if d.get("jabatan") in JABATAN else 0, key=f"mj{k}")
    div = c1.selectbox("Divisi", DIVISI, DIVISI.index(d["divisi"]) if d.get("divisi") in DIVISI else 0, key=f"md{k}")
    kut = c2.text_input("Kutipan / Deskripsi Tugas", d.get("kutipan", ""), key=f"mk{k}")
    up = st.file_uploader("Foto Profil", type=["png", "jpg", "jpeg"], key=f"mu{k}")
    return {"nama": nama, "jabatan": jab, "divisi": div, "kutipan": kut,
            "foto": to_data_uri(up) if up else d.get("foto", "")}


def tab_programs():
    section("Update Cepat Status & Progress (Real-time)")
    for p in S.programs:
        c1, c2, c3 = st.columns([2, 1.3, 2])
        c1.markdown(f"**{esc(p['nama'])}**")
        p["status"] = c2.selectbox("Status", STATUS, STATUS.index(p["status"]),
                                   key=f"qs{p['id']}", label_visibility="collapsed")
        p["progress"] = c3.slider("Progress", 0, 100, p["progress"],
                                  key=f"qp{p['id']}", label_visibility="collapsed")
    section("Tambah Program Kerja")
    with st.form("add_prog", clear_on_submit=True):
        data = prog_fields({}, "new")
        if st.form_submit_button("➕ Tambah", type="primary"):
            if data["nama"].strip():
                S.programs.append({"id": uid(), **data})
                st.success("Program kerja ditambahkan.")
                st.rerun()
            else:
                st.error("Nama kegiatan wajib diisi.")
    section("Edit / Hapus Program Kerja")
    if S.programs:
        pid = st.selectbox("Pilih program", [p["id"] for p in S.programs],
                           format_func=lambda i: next(p["nama"] for p in S.programs if p["id"] == i))
        cur = next(p for p in S.programs if p["id"] == pid)
        with st.form(f"edit_{pid}"):
            data = prog_fields(cur, f"e{pid}")
            c1, c2 = st.columns(2)
            if c1.form_submit_button("💾 Simpan Perubahan", type="primary"):
                if not data["gambar"].strip() or data["gambar"] == "https://picsum.photos/seed/default/600/300":
                    data["gambar"] = cur["gambar"]
                cur.update(data)
                st.success("Perubahan disimpan.")
                st.rerun()
            if c2.form_submit_button("🗑️ Hapus Program"):
                S.programs = [p for p in S.programs if p["id"] != pid]
                st.rerun()


def tab_members():
    section("Tambah Pengurus")
    with st.form("add_mem", clear_on_submit=True):
        data = member_fields({}, "new")
        if st.form_submit_button("➕ Tambah", type="primary"):
            if data["nama"].strip():
                S.members.append({"id": uid(), **data})
                st.rerun()
            else:
                st.error("Nama wajib diisi.")
    section("Edit / Hapus Pengurus")
    if S.members:
        mid = st.selectbox("Pilih pengurus", [m["id"] for m in S.members],
                           format_func=lambda i: next(f"{m['nama']} — {m['jabatan']}" for m in S.members if m["id"] == i))
        cur = next(m for m in S.members if m["id"] == mid)
        with st.form(f"edit_m{mid}"):
            data = member_fields(cur, f"e{mid}")
            c1, c2 = st.columns(2)
            if c1.form_submit_button("💾 Simpan", type="primary"):
                cur.update(data)
                st.success("Data pengurus diperbarui.")
                st.rerun()
            if c2.form_submit_button("🗑️ Hapus"):
                S.members = [m for m in S.members if m["id"] != mid]
                st.rerun()


def tab_content():
    o = S.org
    section("Konten Beranda & Kontak")
    with st.form("form_org"):
        c1, c2 = st.columns(2)
        o["nama"] = c1.text_input("Nama Organisasi", o["nama"])
        o["tagline"] = c2.text_input("Tagline", o["tagline"])
        o["deskripsi"] = st.text_area("Deskripsi", o["deskripsi"])
        o["visi"] = st.text_area("Visi", o["visi"])
        misi = st.text_area("Misi (satu poin per baris)", "\n".join(o["misi"]), height=130)
        o["mitra"] = c1.number_input("Jumlah Mitra", 0, 10000, o["mitra"])
        o["alamat"] = c2.text_input("Alamat Sekretariat", o["alamat"])
        o["email"] = c1.text_input("Email", o["email"])
        o["wa"] = c2.text_input("WhatsApp (format 62xxx)", o["wa"])
        o["instagram"] = c1.text_input("URL Instagram", o["instagram"])
        o["linkedin"] = c2.text_input("URL LinkedIn", o["linkedin"])
        if st.form_submit_button("💾 Simpan Konten", type="primary"):
            o["misi"] = [m.strip() for m in misi.split("\n") if m.strip()]
            st.success("Konten tersimpan.")
            st.rerun()
    section("Pengumuman / Berita")
    with st.form("add_news", clear_on_submit=True):
        c1, c2 = st.columns([2, 1])
        j = c1.text_input("Judul")
        t = c2.text_input("Tanggal", placeholder="30 Okt 2026")
        isi = st.text_area("Isi singkat")
        if st.form_submit_button("➕ Tambah Berita") and j.strip():
            S.news.insert(0, {"id": uid(), "judul": j, "tanggal": t, "isi": isi})
            st.rerun()
    for n in S.news:
        c1, c2 = st.columns([5, 1])
        c1.markdown(f"**{esc(n['judul'])}** — {esc(n['tanggal'])}")
        if c2.button("Hapus", key=f"dn{n['id']}"):
            S.news = [x for x in S.news if x["id"] != n["id"]]
            st.rerun()


def tab_messages():
    section(f"Pesan & Aspirasi Masuk ({len(S.messages)})")
    if not S.messages:
        st.info("Belum ada pesan.")
    for m in S.messages:
        st.markdown(f"<div class='card'><b>{esc(m['nama'])}</b> <small>({esc(m['email'] or '-')})</small>"
                    f"<p style='color:#475569'>{esc(m['pesan'])}</p></div>", unsafe_allow_html=True)
        if st.button("Hapus", key=f"dm{m['id']}"):
            S.messages = [x for x in S.messages if x["id"] != m["id"]]
            st.rerun()


def page_admin():
    if not S.admin:
        admin_login()
        return
    st.title("🛠️ Dashboard Admin")
    t1, t2, t3, t4 = st.tabs(["📋 Program Kerja", "👥 Pengurus", "📝 Konten Web", "📬 Pesan Masuk"])
    with t1:
        tab_programs()
    with t2:
        tab_members()
    with t3:
        tab_content()
    with t4:
        tab_messages()
    st.caption("ℹ️ Data tersimpan di Session State dan akan reset jika browser direfresh / sesi berakhir.")


# ============================ ROUTER ============================
{MENU[0]: page_home, MENU[1]: page_programs, MENU[2]: page_members,
 MENU[3]: page_contact, MENU[4]: page_admin}[page]()

st.markdown("<hr><div style='text-align:center;color:#94A3B8;font-size:.8rem'>"
            f"© 2026 {esc(S.org['nama'])} • Portal Resmi Organisasi</div>", unsafe_allow_html=True)