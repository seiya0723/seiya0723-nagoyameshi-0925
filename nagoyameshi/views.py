from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


# models.pyから Restaurantを importするには
from .models import Restaurant
# models.py から Categoryをimportする。
from .models import Category
# models.py から Review を importする。
from .models import Review
# models.py から Favorite を importする
from .models import Favorite
# models.py から PremiumUser をimportする
from .models import PremiumUser


# forms.py から ReviewForm をimportする。
from .forms import ReviewForm
from .forms import FavoriteForm
from .forms import ReservationForm

from django.db.models import Q

class TopView(View):
    def get(self, request, *args, **kwargs):


        # TODO:ここで検索をする。

        # ↓で name="search" の入力欄の内容を取得する。
        #print(request.GET["search"])

        # name="search"のテキストボックスに店舗Aと入力した時、↓のURLへリクエストが送信される。
        # http://127.0.0.1:8000/?search=店舗A
        #                        ↑ クエリストリング(URLパラメータとも呼ばれる)
        # ↑の入力された内容を元に、検索をする。

        # クエリビルダのオブジェクトを作る
        query = Q()

        # もし検索をしていない場合、request.GET の中に search はないのでエラーになる。    
        if "search" in request.GET:
            print(request.GET["search"])

            # TODO: ここで検索をする。.filter(条件) で条件に一致したデータを取り出せる。 
            # 店舗名が request.GET["search"]と同じ場合 表示する。
            #restaurants = Restaurant.objects.filter(name=request.GET["search"])

            # ↑の場合、店舗名と検索キーワードが一致すれば出てくる。
            # 「和食」と検索した場合、店名が「和食」と完全一致でなければ出てこない。

            # 「和食」と検索した場合、店名が「和食」を含むデータを出す。 
            # フィールド名__icontains とすることで、指定した文字列を含む (大文字小文字の区別はしない) django でも Django でも検索結果は同じ
            # フィールド名__contains とすることで、指定した文字列を含む (大文字小文字の区別をする) django でも Django でも検索結果は違う
            restaurants = Restaurant.objects.filter(name__icontains=request.GET["search"])

            # 「和食　A」と検索した場合。↑の方法では何も出てこない。
            # 「和食　A」を店名に含むデータを取り出す。出てくるのは「和食　A 〇〇店」など、スペースも文字列の一部として扱われているデータのみ。

            # スペース区切りの文字列検索をする。
            # request.GET["search"] を スペースで区切ってリスト型にする必要がある。
            # "和食　A" or "和食 A" → ["和食","A"]

            words = request.GET["search"].replace("　", " ").split()

            for word in words:
                # 検索条件を追加していく。
                query &= Q(name__icontains=word)

        """
            restaurants = Restaurant.objects.filter(query)
        else:
            
            # Restaurant を使って、全データを取り出し、コンテキストに入れてレンダリングする。
            #restaurants = Restaurant.objects.all()

            #                                        ↓ else側では検索条件は空
            restaurants = Restaurant.objects.filter(query)
        """

        # TODO: カテゴリの検索条件を加える

        #query &= Q(category=2)
        # name="category" の値を取り出すには？

        if "category" in request.GET:
            if "" != request.GET["category"]:
                # カテゴリ検索の追加
                query &= Q(category=request.GET["category"])


        restaurants = Restaurant.objects.filter(query)


        # カテゴリの選択肢を作るため、全データを取り出し。contextに与える。
        categories = Category.objects.all()


        # ListViewの場合、 model = Restaurant だが、今回は検索機能を実装させるため、全件呼び出しを直接書く。
        context = { "restaurants":restaurants,
                    "categories":categories,
        }
        
        # TODO:検索結果を含めてレンダリングする
        return render(request,"nagoyameshi/top.html", context)

# pk=1 を引数に実行する。
class RestaurantView(View):
    def get(self, request, pk, *args, **kwargs):
        context = {}
        # pkを使って、 店舗を特定する。
        context["restaurant"]   = Restaurant.objects.filter(id=pk).first()
        # .filter() は戻り値がリスト型。
        # .first() で、モデルオブジェクト1件のみ返すようにする。

        # Review を使って、この店舗のレビューをすべて取り出す。(.all() にすると、別の店のレビューも表示されてしまう。)
        # context["reviews"] = Review.objects.all()
        # Restaurant.idがpkである店舗のレビューだけ取り出す
        context["reviews"] = Review.objects.filter(restaurant=pk)


        return render(request, "nagoyameshi/restaurant.html",context)



# レビューの投稿を受け付けるビュー
class ReviewView(LoginRequiredMixin,View):
    # レビューの投稿(post)
    #                        ↓ Restaurantのid。どの店舗に対してレビューを投稿するか
    def post(self, request, pk, *args, **kwargs):
        # TODO:投稿処理を書く

        # restaurant.htmlのフォームをここでバリデーションして、保存する。
        # クライアントから送信されたデータ request.POST

        # star と contentの2つ
        copied = request.POST.copy()
        copied["user"] = request.user.id
        copied["restaurant"] = pk

        form = ReviewForm(copied)

        print("投稿")

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        # レビューを投稿した後、店舗の詳細ページへリダイレクト
        return redirect("restaurant", pk)


# お気に入りの登録(投稿)を受け付けるビュー
class FavoriteView(LoginRequiredMixin, View):
    #                        ↓ Restaurantのid。どの店舗に対してレビューを投稿するか
    def post(self, request, pk, *args, **kwargs):
        # TODO:投稿処理を書く

        # 送られてきたデータをコピーして、お気に入りしたいユーザーと店舗のidを追加する。
        copied = request.POST.copy()
        copied["user"] = request.user.id
        copied["restaurant"] = pk

        form = FavoriteForm(copied)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)


        # お気に入りを投稿した後、店舗の詳細ページへリダイレクト
        return redirect("restaurant", pk)

# 予約を受け付けるビュー
class ReservationView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        # ====有料会員状態の判定(レビュー、お気に入り、予約に加える)==========================

        # PremiumViewにアクセスしたユーザー(request.user)のデータを取り出す。(DBに対して絞り込みをする。)
        premium_user = PremiumUser.objects.filter(user=request.user).first()

        # 全データ読み込み
        # PremiumUser.objects.all()

        if not premium_user:
            print("有料会員登録をしていません")
            return redirect("mypage")


        # カスタマーIDを元にStripeに問い合わせ
        try:
            subscriptions = stripe.Subscription.list(customer=premium_user.premium_code)
        except:
            print("このカスタマーIDは無効です。")
            premium_user.delete()

            return redirect("mypage")

        is_premium = False

        # ステータスがアクティブであるかチェック。
        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です。")

                is_premium = True
            else:
                print("サブスクリプションが無効です。")


        if not is_premium:
            print("有料会員登録をしていない")
            return redirect("mypage")
        # ====有料会員状態の判定==========================            

        # TODO: 有料会員登録をした人向けの処理        
        # TODO:予約の登録をする
    
        copied = request.POST.copy()
        copied["user"] = request.user.id
        copied["restaurant"] = pk

        form = ReservationForm(copied)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        
        # 予約した店舗にリダイレクト
        return redirect("restaurant", pk)


# マイページを表示するビュー
class MypageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        #           ↑ アクセスしてきた人のユーザー情報が含まれている。 request.user
        context = {}
        # 自分がお気に入りした店舗のデータを取り出す。Favoriteモデルを使って自分のデータだけ取り出す。
        context["favorites"] = Favorite.objects.filter(user=request.user)

        # 自分以外のユーザーのお気に入り情報が取れてしまう。
        # Favorite.objects.all()

        # 有料会員登録をしているか？
        premium_user = PremiumUser.objects.filter(user=request.user).first()

        if premium_user:
            context["is_premium"] = True
        else:
            context["is_premium"] = False

        return render(request, "nagoyameshi/mypage.html", context)



# Stripeの処理 #
from django.conf import settings
from django.urls import reverse_lazy
import stripe

# APIキーをセットする。
stripe.api_key  = settings.STRIPE_API_KEY


# 有料会員登録のボタンを押して実行されるビュー
class CheckoutView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):

        # セッションを作る 2~3
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': settings.STRIPE_PRICE_ID,
                    'quantity': 1,
                },
            ],
            payment_method_types=['card'],
            mode='subscription',
            #             ↓でカード決済した後のリダイレクト先URL(7の箇所)を指定している。今回は決済成功時に、SuccessViewを呼び出したい。
            success_url=request.build_absolute_uri(reverse_lazy("success")) + '?session_id={CHECKOUT_SESSION_ID}',
            #              ↓カード決済をやめるときにリダイレクトする
            cancel_url=request.build_absolute_uri(reverse_lazy("mypage")),
        )

        # セッションid
        print( checkout_session["id"] )

        # 決済ページにリダイレクトをする4~5
        return redirect(checkout_session.url)

#checkout    = CheckoutView.as_view()

# 8の決済後。Django側でStripeに問い合わせてチェック。
class SuccessView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        # パラメータにセッションIDがあるかチェック
        if "session_id" not in request.GET:
            print("セッションIDがありません。")
            return redirect("mypage")


        # そのセッションIDは有効であるかチェック。
        try:
            checkout_session_id = request.GET['session_id']
            checkout_session    = stripe.checkout.Session.retrieve(checkout_session_id)
        except:
            print( "このセッションIDは無効です。")
            return redirect("mypage")

        # セッションのデータを取り出す。
        print(checkout_session)

        # statusをチェックする。未払であれば拒否する。(未払いのsession_idを入れられたときの対策)
        if checkout_session["payment_status"] != "paid":
            print("未払い")
            return redirect("mypage")

        print("支払い済み")


        # 有効であれば、セッションIDからカスタマーIDを取得。
        # PremiumUserモデルへ記録する。
        """
        request.user.customer   = checkout_session["customer"]
        request.user.save()
        """

        premium_user = PremiumUser()
        # このカスタマーIDを使って有料会員登録をしたかどうかを判定する。
        premium_user.premium_code = checkout_session["customer"]
        premium_user.user = request.user
        premium_user.save()

        print("有料会員登録しました！")

        return redirect("mypage")

#success     = SuccessView.as_view()



# サブスクリプションの操作関係(サブスクを途中でやめる用のビュー) 
class PortalView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        # サブスクリプション登録をしている人か？
        premium_user = PremiumUser.objects.filter(user=request.user).first()


        if not premium_user:
            print( "有料会員登録されていません")
            return redirect("mypage")

        # ユーザーモデルに記録しているカスタマーIDを使って、ポータルサイトへリダイレクト
        portalSession   = stripe.billing_portal.Session.create(
            customer    = premium_user.premium_code,
            return_url  = request.build_absolute_uri(reverse_lazy("mypage")),
        )

        return redirect(portalSession.url)

#portal      = PortalView.as_view()





# 有料会員登録をしているのかどうかを判定する
class PremiumView(View):
    def get(self, request, *args, **kwargs):

        # ====有料会員状態の判定(レビュー、お気に入り、予約に加える)==========================

        # PremiumViewにアクセスしたユーザー(request.user)のデータを取り出す。(DBに対して絞り込みをする。)
        premium_user = PremiumUser.objects.filter(user=request.user).first()

        # 全データ読み込み
        # PremiumUser.objects.all()

        if not premium_user:
            print("有料会員登録をしていません")
            return redirect("mypage")


        # カスタマーIDを元にStripeに問い合わせ
        try:
            subscriptions = stripe.Subscription.list(customer=premium_user.premium_code)
        except:
            print("このカスタマーIDは無効です。")
            premium_user.delete()

            return redirect("mypage")

        is_premium = False

        # ステータスがアクティブであるかチェック。
        for subscription in subscriptions.auto_paging_iter():
            if subscription.status == "active":
                print("サブスクリプションは有効です。")

                is_premium = True
            else:
                print("サブスクリプションが無効です。")


        if not is_premium:
            print("有料会員登録をしていない")
            return redirect("mypage")
        # ====有料会員状態の判定==========================            

        # TODO: 有料会員登録をした人向けの処理



        return redirect("mypage")
