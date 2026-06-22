import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date
from app.database import engine, SessionLocal, Base
from app.models import Pet, Vaccine, Allergy, MedicalRecord, ClinicalExam, LabExam, Diagnosis


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(Pet).first():
            print("Database already has data. Skipping seed.")
            return

        pet1 = Pet(
            name="旺财",
            species="犬",
            breed="金毛寻回犬",
            gender="公",
            age=3.5,
            weight=28.0,
            fur_color="金色",
            neutered=True,
            owner_name="张三",
            owner_phone="13800138001",
        )
        pet2 = Pet(
            name="咪咪",
            species="猫",
            breed="英国短毛猫",
            gender="母",
            age=2.0,
            weight=4.5,
            fur_color="蓝灰色",
            neutered=False,
            owner_name="李四",
            owner_phone="13900139002",
        )
        pet3 = Pet(
            name="豆豆",
            species="犬",
            breed="柯基犬",
            gender="公",
            age=1.5,
            weight=12.0,
            fur_color="黄白色",
            neutered=False,
            owner_name="王五",
            owner_phone="13700137003",
        )
        db.add_all([pet1, pet2, pet3])
        db.commit()
        db.refresh(pet1)
        db.refresh(pet2)
        db.refresh(pet3)

        vaccine1 = Vaccine(
            pet_id=pet1.id,
            vaccine_type="狂犬",
            injection_date=date(2025, 1, 15),
            brand="梅里亚",
            batch_no="RB20250101",
            next_date=date(2026, 1, 15),
        )
        vaccine2 = Vaccine(
            pet_id=pet1.id,
            vaccine_type="犬五联",
            injection_date=date(2025, 2, 20),
            brand="英特威",
            batch_no="D520250201",
            next_date=date(2026, 2, 20),
        )
        vaccine3 = Vaccine(
            pet_id=pet2.id,
            vaccine_type="猫三联",
            injection_date=date(2025, 3, 10),
            brand="英特威",
            batch_no="C320250301",
            next_date=date(2026, 3, 10),
        )
        db.add_all([vaccine1, vaccine2, vaccine3])

        allergy1 = Allergy(
            pet_id=pet1.id,
            allergy_type="药物",
            allergen="青霉素",
            reaction="皮肤红肿、瘙痒",
            severity="中度",
        )
        allergy2 = Allergy(
            pet_id=pet2.id,
            allergy_type="食物",
            allergen="鸡肉",
            reaction="呕吐、腹泻",
            severity="轻度",
        )
        db.add_all([allergy1, allergy2])

        record1 = MedicalRecord(
            pet_id=pet1.id,
            visit_date=date(2025, 5, 10),
            chief_complaint="食欲下降、精神萎靡3天",
            present_illness="3天前开始食欲下降，饮水量减少，精神萎靡，偶有咳嗽",
            past_illness="无重大病史，定期驱虫",
            notes="建议进一步检查",
        )
        record2 = MedicalRecord(
            pet_id=pet2.id,
            visit_date=date(2025, 5, 12),
            chief_complaint="频繁挠耳朵",
            present_illness="近一周频繁挠右耳，耳道有异味分泌物",
            past_illness="曾患猫癣，已治愈",
            notes="需排除耳螨",
        )
        db.add_all([record1, record2])
        db.commit()
        db.refresh(record1)
        db.refresh(record2)

        clinical1 = ClinicalExam(
            record_id=record1.id,
            temperature=39.5,
            heart_rate=120,
            respiratory_rate=30,
            weight=27.5,
            body_condition_score=5,
            mucous_membrane_color="粉红色",
            lymph_node_abnormality="下颌淋巴结轻度肿大",
            cardio_pulmonary_auscultation="肺区可闻湿啰音",
        )
        clinical2 = ClinicalExam(
            record_id=record2.id,
            temperature=38.8,
            heart_rate=180,
            respiratory_rate=28,
            weight=4.3,
            body_condition_score=4,
            mucous_membrane_color="粉红色",
            lymph_node_abnormality="未见异常",
            cardio_pulmonary_auscultation="心音正常",
        )
        db.add_all([clinical1, clinical2])

        lab1 = LabExam(
            record_id=record1.id,
            exam_type="血常规",
            result_data={
                "WBC": 18.5,
                "RBC": 6.2,
                "HGB": 140,
                "PLT": 210,
                "NEU%": 82,
                "LYM%": 12,
            },
            notes="白细胞升高，中性粒细胞比例偏高，提示感染",
        )
        lab2 = LabExam(
            record_id=record2.id,
            exam_type="皮肤刮片",
            result_data={
                "findings": "可见螨虫成虫及虫卵",
                "type": "耳螨",
            },
            notes="确诊耳螨感染",
        )
        db.add_all([lab1, lab2])

        diagnosis1 = Diagnosis(
            record_id=record1.id,
            icd_code="J98.4",
            diagnosis_name="肺炎",
            severity_level="中度",
            notes="建议住院输液治疗，抗生素+止咳化痰",
        )
        diagnosis2 = Diagnosis(
            record_id=record2.id,
            icd_code="B88.0",
            diagnosis_name="耳螨感染",
            severity_level="轻度",
            notes="外用驱螨药物，1周后复查",
        )
        db.add_all([diagnosis1, diagnosis2])

        db.commit()
        print("Sample data inserted successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error inserting sample data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
