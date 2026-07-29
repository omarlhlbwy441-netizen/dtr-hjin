"""
╔══════════════════════════════════════════════════════════════════╗
║  Rafeeq Kernel v2.3.0 — VideoArchitect Agent                   ║
║  وكيل توليد وتحرير الفيديو                                       ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import json
import uuid
import subprocess
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class VideoArchitect:
    """وكيل متخصص في توليد وتحرير الفيديو"""

    VIDEO_TEMPLATES = {
        "explainer": {
            "name": "Explainer Video",
            "description": "فيديو توضيحي مع نصوص متحركة",
            "duration": 60,
            "style": "modern",
            "scenes": ["intro", "problem", "solution", "features", "cta"]
        },
        "tutorial": {
            "name": "Tutorial Video",
            "description": "فيديو تعليمي خطوة بخطوة",
            "duration": 300,
            "style": "clean",
            "scenes": ["intro", "step1", "step2", "step3", "summary"]
        },
        "promo": {
            "name": "Promotional Video",
            "description": "فيديو ترويجي للمنتجات",
            "duration": 30,
            "style": "dynamic",
            "scenes": ["hook", "product", "benefits", "social_proof", "cta"]
        },
        "story": {
            "name": "Story Video",
            "description": "فيديو سرد قصصي",
            "duration": 120,
            "style": "cinematic",
            "scenes": ["setup", "conflict", "climax", "resolution", "message"]
        }
    }

    def __init__(self):
        self.videos_dir = Path("videos")
        self.videos_dir.mkdir(exist_ok=True)
        self.generated_videos = []
        self.ffmpeg_available = self._check_ffmpeg()

    def _check_ffmpeg(self) -> bool:
        """التحقق من توفر FFmpeg"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def list_templates(self) -> List[Dict]:
        return [{"id": k, **v} for k, v in self.VIDEO_TEMPLATES.items()]

    def generate_video(self, template_type: str, title: str, script: Optional[str] = None, 
                       custom_config: Optional[Dict] = None) -> Dict[str, Any]:
        """توليد فيديو كامل"""
        if template_type not in self.VIDEO_TEMPLATES:
            return {"status": "error", "message": f"Template '{template_type}' not found"}

        template = self.VIDEO_TEMPLATES[template_type]
        video_id = str(uuid.uuid4())[:8]
        safe_title = title.replace(" ", "_").lower()
        video_dir = self.videos_dir / f"{safe_title}_{video_id}"
        video_dir.mkdir(parents=True, exist_ok=True)

        config = {**template, **(custom_config or {})}

        files_generated = []

        # 1. Video Script
        script_content = script or self._generate_script(template_type, title, config)
        (video_dir / "script.txt").write_text(script_content, encoding="utf-8")
        files_generated.append("script.txt")

        # 2. Storyboard JSON
        storyboard = self._generate_storyboard(template_type, config)
        (video_dir / "storyboard.json").write_text(
            json.dumps(storyboard, indent=2, ensure_ascii=False), 
            encoding="utf-8"
        )
        files_generated.append("storyboard.json")

        # 3. Video Generation (if FFmpeg available)
        video_path = None
        if self.ffmpeg_available:
            video_path = self._render_video(video_dir, storyboard, config)
            if video_path:
                files_generated.append(video_path.name)

        # 4. Config
        cfg = json.dumps({
            "video_id": video_id, "title": title, "type": template_type,
            "duration": config.get("duration", 60),
            "ffmpeg_used": self.ffmpeg_available,
            "created_at": datetime.utcnow().isoformat(),
            "files": files_generated
        }, indent=2, ensure_ascii=False)
        (video_dir / "video.json").write_text(cfg, encoding="utf-8")
        files_generated.append("video.json")

        video_info = {
            "status": "success", "video_id": video_id, "title": title,
            "type": template_type, "directory": str(video_dir),
            "files": files_generated,
            "video_path": str(video_path) if video_path else None,
            "ffmpeg_available": self.ffmpeg_available,
            "created_at": datetime.utcnow().isoformat()
        }
        self.generated_videos.append(video_info)
        return video_info

    def _generate_script(self, template_type: str, title: str, config: Dict) -> str:
        """توليد نص الفيديو"""
        scenes = config.get("scenes", [])
        script_parts = [f"# سيناريو: {title}", f"# النوع: {template_type}", f"# المدة: {config.get('duration', 60)} ثانية", "", "---", ""]

        scene_scripts = {
            "intro": f"[المشهد الافتتاحي - 5 ثواني]\n\nمرحباً! أنا رفيق — رفيقك الذكي.\nاليوم سأتحدث عن: {title}\n",
            "problem": "[مشكلة - 10 ثواني]\n\nهل واجهت صعوبة في...\nهل تأخرت في إنجاز مشاريعك...\n",
            "solution": "[الحل - 15 ثانية]\n\nمع رفيق، كل شيء يتغير!\nنظام ذكاء اصطناعي متكامل...\n",
            "features": "[المميزات - 20 ثانية]\n\n✅ وكلاء ذكاء متخصصين\n✅ تطور ذاتي\n✅ بناء تلقائي\n✅ مراقبة كاملة\n",
            "cta": "[دعوة للعمل - 10 ثواني]\n\nابدأ رحلتك مع رفيق الآن!\nزورنا على: rafeeq.ai\n",
            "hook": "[الخطاف - 3 ثواني]\n\nانتظر! قبل أن تغادر...\n",
            "product": "[المنتج - 10 ثواني]\n\nتعرف على {title}\nالمنتج الذي سيغير طريقة عملك\n",
            "benefits": "[الفوائد - 10 ثواني]\n\n⚡ سرعة فائقة\n🎯 دقة عالية\n💰 توفير التكاليف\n",
            "social_proof": "[إثبات اجتماعي - 5 ثواني]\n\nآلاف المستخدمين يثقون بنا!\n",
            "setup": "[الإعداد - 15 ثانية]\n\nفي يوم من الأيام...\nكان هناك مطور طموح...\n",
            "conflict": "[الصراع - 20 ثانية]\n\nواجه تحديات كبيرة...\nلكنه لم يستسلم...\n",
            "climax": "[ذروة القصة - 30 ثانية]\n\nاكتشف رفيق!\nالأداة التي غيّرت كل شيء...\n",
            "resolution": "[الحل - 20 ثانية]\n\nوالآن...\nأصبح من أفضل المطورين في العالم!\n",
            "message": "[الرسالة - 15 ثانية]\n\nالرسالة: لا تستسلم أبداً!\nمع رفيق، كل شيء ممكن\n",
            "step1": "[الخطوة 1 - 60 ثانية]\n\nأولاً: افتح التطبيق\nثم اختر الوكيل المناسب...\n",
            "step2": "[الخطوة 2 - 60 ثانية]\n\nثانياً: اكتب طلبك\nسيقوم الوكيل بالباقي...\n",
            "step3": "[الخطوة 3 - 60 ثانية]\n\nأخيراً: راجع النتيجة\nواستمتع بالجودة!\n",
            "summary": "[الملخص - 60 ثانية]\n\nلنلخّص ما تعلمناه...\nرفيق = قوة + سرعة + جودة\n"
        }

        for scene in scenes:
            if scene in scene_scripts:
                script_parts.append(scene_scripts[scene])
                script_parts.append("")

        script_parts.append("---")
        script_parts.append("")
        script_parts.append("# ملاحظات الإنتاج:")
        script_parts.append("- الموسيقى: حماسية / هادئة حسب المشهد")
        script_parts.append("- التأثيرات: انتقالات سلسة")
        script_parts.append("- النصوص: عربية، خط Tajawal")
        script_parts.append("- الألوان: أزرق + بنفسجي + أخضر")

        return "\n".join(script_parts)

    def _generate_storyboard(self, template_type: str, config: Dict) -> Dict:
        """توليد storyboard للفيديو"""
        scenes = config.get("scenes", [])
        duration = config.get("duration", 60)
        scene_duration = duration // max(len(scenes), 1)

        storyboard = {
            "template": template_type,
            "total_duration": duration,
            "fps": 30,
            "resolution": "1920x1080",
            "scenes": []
        }

        scene_visuals = {
            "intro": {"bg": "gradient_dark", "elements": ["logo", "title"], "animation": "fade_in"},
            "problem": {"bg": "gradient_red", "elements": ["icon_warning", "text"], "animation": "slide_left"},
            "solution": {"bg": "gradient_blue", "elements": ["icon_check", "text"], "animation": "slide_right"},
            "features": {"bg": "gradient_purple", "elements": ["cards", "icons"], "animation": "stagger"},
            "cta": {"bg": "gradient_green", "elements": ["button", "url"], "animation": "pulse"},
            "hook": {"bg": "solid_dark", "elements": ["text_large"], "animation": "zoom_in"},
            "product": {"bg": "gradient_blue", "elements": ["product_image", "title"], "animation": "fade_in"},
            "benefits": {"bg": "gradient_purple", "elements": ["bullet_points", "icons"], "animation": "stagger"},
            "social_proof": {"bg": "gradient_gold", "elements": ["stars", "avatars"], "animation": "fade_in"},
            "setup": {"bg": "gradient_dark", "elements": ["scene_image", "narration"], "animation": "fade_in"},
            "conflict": {"bg": "gradient_red", "elements": ["tension_visual", "text"], "animation": "shake"},
            "climax": {"bg": "gradient_blue", "elements": ["hero_image", "title"], "animation": "zoom_in"},
            "resolution": {"bg": "gradient_green", "elements": ["success_image", "text"], "animation": "fade_in"},
            "message": {"bg": "gradient_purple", "elements": ["quote", "author"], "animation": "fade_in"},
            "step1": {"bg": "gradient_blue", "elements": ["screenshot", "annotation"], "animation": "slide_up"},
            "step2": {"bg": "gradient_blue", "elements": ["screenshot", "annotation"], "animation": "slide_up"},
            "step3": {"bg": "gradient_blue", "elements": ["screenshot", "annotation"], "animation": "slide_up"},
            "summary": {"bg": "gradient_dark", "elements": ["checklist", "cta"], "animation": "stagger"}
        }

        for i, scene in enumerate(scenes):
            visual = scene_visuals.get(scene, {"bg": "gradient_dark", "elements": ["text"], "animation": "fade_in"})
            storyboard["scenes"].append({
                "id": i + 1,
                "name": scene,
                "duration": scene_duration,
                "start_time": i * scene_duration,
                "end_time": (i + 1) * scene_duration,
                "background": visual["bg"],
                "elements": visual["elements"],
                "animation": visual["animation"],
                "transition": "fade" if i == 0 else "slide"
            })

        return storyboard

    def _render_video(self, video_dir: Path, storyboard: Dict, config: Dict) -> Optional[Path]:
        """تصيير الفيديو باستخدام FFmpeg"""
        if not self.ffmpeg_available:
            return None

        output_path = video_dir / "output.mp4"

        # Create a simple color video with text overlay
        # This is a placeholder - real implementation would use complex FFmpeg filters
        try:
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", f"color=c=0x0f172a:s=1920x1080:d={config.get('duration', 60)}",
                "-vf", "drawtext=text='Rafeeq VideoArchitect':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                str(output_path)
            ]
            subprocess.run(cmd, capture_output=True, timeout=60)
            return output_path if output_path.exists() else None
        except Exception as e:
            print(f"Video rendering failed: {e}")
            return None

    def list_videos(self):
        return self.generated_videos


video_architect = VideoArchitect()
def get_video_architect():
    return video_architect
