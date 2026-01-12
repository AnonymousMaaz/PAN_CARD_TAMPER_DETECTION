# **PAN CARD TAMPERING DETECTION**
> The purpose of this project is to detect tampering of PAN card using computer vision. This project will help different organization in detecting whether the id i.e the PAN card provided to them by their employees or customers or anyone is original or not
> For this project we will calculate the **Structural Similarity** of the original PAN Card and the PAN Card uploaded by the user.


# 🆔 PAN Card Tampering Detection using Structural Similarity (SSIM)

To detect whether a **PAN card is original or tampered**, we need a way to **compare two images**:
1. The **original PAN card**
2. The **PAN card uploaded by the user**

One of the best techniques for this is **Structural Similarity Index (SSIM)**.

Let’s understand it **from zero to advanced**, in **simple language**, with **real-world examples**, and then see **how to use it in Python with `skimage`**.

---

## 📌 What is Structural Similarity (SSIM)?

### 🔍 Simple Definition
**Structural Similarity (SSIM)** is a method used to **measure how similar two images are** based on:
- **Structure**
- **Brightness**
- **Contrast**

It gives a **score between -1 and 1**:
- `1.0` → Images are **exactly identical**
- `0.0` → Images are **not similar**
- `< 0` → Images are **completely different**

In real applications:
- **Above 0.9** → Very similar (likely original)
- **0.7 – 0.9** → Slightly altered
- **Below 0.7** → Possibly tampered

---

## 🧠 Why Not Just Compare Pixel Values?

### ❌ Pixel Comparison Problem
If we compare two images pixel by pixel:
- Slight lighting change
- Small rotation
- Image compression

👉 Even a **real PAN card photo** can look different!

### ✅ SSIM Solution
SSIM **thinks like a human eye**, not a computer.

Humans don’t see pixels — we see:
- Shapes
- Text
- Layout
- Patterns

SSIM compares these **structures**, not just raw pixels.

---

## 🌍 Real-World Layman Example

### 📄 Example: Photocopy vs Original PAN Card
Imagine:
- You have an **original PAN card**
- You make a **photocopy**

Even if:
- The brightness changes
- Colors fade slightly

👉 You can still **recognize it as the same PAN card**

SSIM works the same way.

---

## 🔎 What Exactly Does SSIM Compare?

SSIM is made of **three components**:

---

### 1️⃣ **Luminance (Brightness)**
- Checks if one image is **brighter or darker** than the other
- Example:
  - One PAN image is taken in sunlight
  - Another in indoor lighting

SSIM tolerates this difference.

---

### 2️⃣ **Contrast**
- Checks difference between **dark and light regions**
- Example:
  - Text clarity
  - Logo sharpness

A forged PAN card may have **blurred or altered contrast**.

---

### 3️⃣ **Structure**
- Most important part
- Checks:
  - Position of text
  - Layout of photo
  - Alignment of PAN number, DOB, signature

👉 **Tampering breaks structure**

---

### 📐 SSIM Formula (Conceptual)
**SSIM(x, y) = (luminance) × (contrast) × (structure)**


You don’t need to calculate it manually — libraries do that.

---

## 🆔 Why SSIM is Perfect for PAN Card Tampering Detection

| Tampering Type | SSIM Reaction |
|---------------|--------------|
| Name changed | Score ↓ |
| Photo replaced | Score ↓ |
| PAN number edited | Score ↓ |
| Minor lighting change | Score stays high |
| Image compression | Score stays high |

---

## 🧪 Example Scenario

### Original PAN Card
- Name: Rahul Sharma
- PAN: ABCDE1234F

### Tampered PAN Card
- Name changed to: Rohit Sharma

👉 Structure changes in **text region**
👉 SSIM score drops

---

## 🧰 Using SSIM in Python (skimage)

### 📦 Install Required Libraries
```bash
pip install scikit-image opencv-python
