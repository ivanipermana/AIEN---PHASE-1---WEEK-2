"""Peserta hanya perlu mengedit 3 TODO di file ini."""


def complete_trace(trace, duration_ms, status):
    """TODO 1: isi trace['duration_ms'] dan trace['status'].

    duration_ms sudah diukur aplikasi. status: ok, degraded, atau error.
    Jangan menghapus request_id, spans, dan metadata lainnya.
    """
    # Ganti dua nilai placeholder dengan parameter yang tersedia.
    trace['duration_ms'] = None
    trace['status'] = 'unknown'
    return trace


def choose_document_version(manifest):
    """TODO 2: pilih versi aktif dari manifest, bukan versi yang dipatok.

    Inspect data/manifest.json. Gunakan key current_version.
    Validasi versi di lab_core/retrieval.py sudah disediakan.
    """
    return 'v1'  # BUG: versi ini sudah kedaluwarsa.


def fallback_for_timeout(error, faq_url):
    """TODO 3: return pesan gangguan dengan tautan FAQ resmi.

    error adalah ModelTimeout, setelah retry terbatas habis.
    Pesan harus menyebut 'gangguan' dan menyertakan faq_url.
    Jangan mengarang jawaban kebijakan saat model gagal.
    """
    raise error  # BUG: kegagalan model langsung menjadi kegagalan aplikasi.
