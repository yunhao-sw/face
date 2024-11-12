from flask import Flask, request, jsonify
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
import numpy as np

app = Flask(__name__)

# 加载 ArcFace 人脸识别模型的 pipeline
arc_face_recognition_func = pipeline(Tasks.face_recognition, 'damo/cv_ir50_face-recognition_arcface')

@app.route('/face_similarity', methods=['POST'])
def face_similarity():
    data = request.get_json(force=True)
    img1 = data.get('img1')
    img2 = data.get('img2')
    
    if not img1 or not img2:
        return jsonify({'error': 'Please provide both img1 and img2 URLs'}), 400

    try:
        # 使用模型计算两个图片的嵌入向量
        emb1 = arc_face_recognition_func(img1)[OutputKeys.IMG_EMBEDDING]
        emb2 = arc_face_recognition_func(img2)[OutputKeys.IMG_EMBEDDING]
        
        # 计算余弦相似度
        sim = np.dot(emb1[0], emb2[0])
        similarity = sim.item()  # 将numpy标量转换为Python标量
        return jsonify({
            'face_cosine_similarity': f'{similarity:.3f}',
            'img1': img1,
            'img2': img2
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)