from django import forms

# models.pyからReviewをimportする
from .models import Review
# models.pyからFavoriteをimportする
from .models import Favorite
# models.pyからReservationをimportする
from .models import Reservation

# Reviewを元に、バリデーションルール(フォームクラス)を作る
class ReviewForm(forms.ModelForm):
    class Meta:
        # 何のモデルの何のフィールドをバリデーションルールとするか
        model = Review
        fields = ["user","restaurant","star","content"]


# Favoriteを元に、バリデーションルール(フォームクラス)を作る
class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ["user","restaurant"]

# Reservationを元にバリデーションルールを作る。
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["user","restaurant","datetime","headcount"]