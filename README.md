# Algolia API Key Scanner <img src="https://avatars.githubusercontent.com/u/2034458?s=200&v=4" alt="logo" width="20"/>

A security analysis and testing tool for Algolia API keys.

[English](#overview) | [Türkçe](#genel-bakış)

## Overview [![Türkçe](https://flagcdn.com/w20/gb.png)](#overview)

The Algolia API Key Scanner is a comprehensive tool designed to:

1. Analyze the permissions associated with Algolia API keys
2. Test what operations can actually be performed with a given key
3. Identify potential security vulnerabilities (like admin keys)
4. Provide an interactive interface to work with Algolia indices

This tool is valuable for security researchers, developers, and system administrators who want to verify the security posture of their Algolia implementation or analyze API keys discovered during security assessments.

## Features

- **API Key Analysis**: Decode and analyze API key permissions (ACL)
- **Permission Testing**: Verify what operations the key can actually perform 
- **Interactive Mode**: Perform common Algolia operations with the analyzed key
- **Security Highlighting**: Clearly identify admin keys and excessive permissions
- **Object Exploration**: Browse and search Algolia indices

## Available Actions

Depending on the API key's permissions, you can:

- **Search Objects**: Query indices and view detailed results
- **List Indices**: See all available indices with metadata and sample objects
- **Get Settings**: View configuration settings for indices
- **Delete Objects**: Remove objects from indices (if permitted)

## Installation

```bash
# Clone the repository
git clone https://github.com/Xfci/algolia-api-key-scanner.git
cd algolia-api-key-scanner
```

```bash
# Install dependencies.
pip install requests colorama
```

## Usage

```bash
python algolia_api_key_scanner.py
```

Follow the interactive prompts:

1. Enter the Algolia App ID
2. Enter the Algolia API Key
3. Enter the Algolia Index Name
4. Wait for the key analysis to complete
5. Choose from available actions based on the key's permissions

## Example Output

```
==========================================
ALGOLIA API KEY ANALYSIS
==========================================

Key Creation Date: 2024-05-06 10:32:57
Key Expiry: Never (no expiration)

ACL Permissions:
search, listIndexes, settings

Permission Analysis:
- Can perform search operations
- Can list all indices
- Can read index settings

Operation Tests:
- Can Search: Yes
- Can List Indices: Yes
- Can Read Settings: Yes
- Can Write: No
- Can Delete: No

==========================================

Available Actions:
1. Search objects
2. List indices
3. Get index settings
q. Quit

What do you want to do?
```

## Security Considerations

- The tool clearly highlights admin keys with a "VULNERABLE" warning
- API keys with write/delete permissions are flagged with warnings
- Always use this tool with proper authorization
- Avoid using admin API keys in production environments

## Use Cases

- **Security Audits**: Verify your Algolia API keys are properly restricted
- **API Key Analysis**: Understand what permissions a key has before using it
- **Development Support**: Test Algolia functionality during application development
- **Data Exploration**: Quickly browse Algolia indices and understand their structure

## Disclaimer

This tool is intended for legitimate security research and development purposes only. Always ensure you have proper authorization before scanning or testing any API keys or systems.

---

# Algolia API Anahtar Tarayıcısı 

Algolia API anahtarları için güvenlik analizi ve test aracı.

## Genel Bakış [![Türkçe](https://flagcdn.com/w20/tr.png)](#genel-bakış)

Algolia API Anahtar Tarayıcısı aşağıdaki işlevleri gerçekleştirmek üzere tasarlanmıştır:

1. Algolia API anahtarlarıyla ilişkili izinleri analiz etmek
2. Belirli bir anahtarla hangi işlemlerin gerçekten gerçekleştirilebileceğini test etmek
3. Potansiyel güvenlik açıklarını (admin anahtarları gibi) belirlemek
4. Algolia indeksleriyle çalışmak için etkileşimli bir arayüz sağlamak

Bu araç, Algolia uygulamalarının güvenliğini doğrulamak veya güvenlik değerlendirmeleri sırasında keşfedilen API anahtarlarını analiz etmek isteyen güvenlik araştırmacıları, geliştiriciler ve sistem yöneticileri için kolaylık sağlar.

## Özellikler

- **API Anahtar Analizi**: API anahtar izinlerini (ACL) çözme ve analiz etme
- **İzin Testi**: Anahtarın gerçekten hangi işlemleri gerçekleştirebileceğini doğrulama
- **Etkileşimli Mod**: Analiz edilen anahtarla yaygın Algolia işlemlerini gerçekleştirme
- **Güvenlik Vurgulama**: Admin anahtarları ve aşırı izinleri açıkça tanımlama
- **Nesne Keşfi**: Algolia indekslerini göz atma ve arama

## Kullanılabilir İşlemler

API anahtarının izinlerine bağlı olarak şunları yapabilirsiniz:

- **Nesneleri Arama**: İndeksleri sorgulama ve ayrıntılı sonuçları görüntüleme
- **İndeksleri Listeleme**: Tüm mevcut indeksleri meta verileri ve örnek nesnelerle görme
- **Ayarları Alma**: İndeksler için yapılandırma ayarlarını görüntüleme
- **Nesneleri Silme**: İndekslerden nesneleri kaldırma (izin verilirse)

## Kurulum

```bash
# Repoyu klonla
git clone https://github.com/yourusername/algolia-api-key-scanner.git
cd algolia-api-key-scanner
```

```bash
# Gerekli kütüphaneleri indir
pip install requests colorama
```

## Kullanım

```bash
python algolia_api_key_scanner.py
```

Komutları takip edin:

1. Algolia Uygulama ID'sini girin
2. Algolia API Anahtarını girin
3. Algolia İndeks Adını girin
4. Anahtar analizi tamamlanana kadar bekleyin
5. Anahtarın izinlerine göre mevcut işlemlerden seçim yapın

## Örnek Çıktı

```
==========================================
ALGOLIA API KEY ANALYSIS
==========================================

Key Creation Date: 2024-05-06 10:32:57
Key Expiry: Never (no expiration)

ACL Permissions:
search, listIndexes, settings

Permission Analysis:
- Can perform search operations
- Can list all indices
- Can read index settings

Operation Tests:
- Can Search: Yes
- Can List Indices: Yes
- Can Read Settings: Yes
- Can Write: No
- Can Delete: No

==========================================

Available Actions:
1. Search objects
2. List indices
3. Get index settings
q. Quit

What do you want to do?
```

## Güvenlik Hususları

- Araç, admin anahtarlarını "VULNERABLE" uyarısıyla açıkça vurgular
- Yazma/silme izinlerine sahip API anahtarları uyarılarla işaretlenir
- Bu aracı her zaman uygun yetkilendirme ile kullanın
- Gerçek ortamlarda admin API anahtarlarını kullanırken dikkat edin

## Kullanım Senaryoları

- **Güvenlik Denetimleri**: Algolia API anahtarlarınızın düzgün şekilde kısıtlandığını doğrulama
- **API Anahtar Analizi**: Bir anahtarı kullanmadan önce hangi izinlere sahip olduğunu anlama
- **Geliştirme Desteği**: Uygulama geliştirme sırasında Algolia işlevselliğini test etme
- **Veri Keşfi**: Algolia indekslerine hızlıca göz atma ve yapılarını anlama

## Sorumluluk Reddi

Bu araç, yalnızca meşru güvenlik araştırmaları ve geliştirme amaçları için tasarlanmıştır. Herhangi bir API anahtarını veya sistemi taramadan veya test etmeden önce her zaman yetkilendirmeye sahip olduğunuzdan emin olun.
