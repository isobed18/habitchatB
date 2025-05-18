from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from habits.forms import HabitForm
from django.contrib import messages
from habits.models import Habit
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from datetime import date

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_habits(request):
    habits = Habit.objects.filter(user=request.user)
    habit_list = [
        {
            'id': habit.id,
            'name': habit.name,
            'habit_type': habit.habit_type,
            'target_count': habit.target_count,
            'target_time': habit.target_time,
            'total_time': str(habit.total_time) if habit.total_time else None,
            'completed_count': habit.completed_count,  # Tamamlanan gün sayısı
            'last_completed_date': habit.last_completed_date,  # Son tamamlanma tarihi
            'streak': habit.streak,
            'count': habit.count,
            'frequency': habit.frequency,
        } for habit in habits
    ]
    return Response({'habits': habit_list})




# 2. API: Yeni bir alışkanlık ekle
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_habit(request):
    form = HabitForm(request.data)
    if form.is_valid():
        habit = form.save(commit=False)
        habit.user = request.user
        habit.save()
        return Response({'message': 'Habit added successfully!'})
    return Response({'errors': form.errors}, status=400)

# 3. API: Belirli bir alışkanlığı güncelle

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    original_target_count = habit.target_count
    today = date.today()  # Bugünü date nesnesi olarak al
    print(request.data.items())
    print(habit.count)
    print(habit.target_count)
    for key, value in request.data.items():
        
        if key == 'name' :
            habit.name = value
        elif key == 'count' :
            habit.count = value

        elif key == 'target_count':
            value = int(value) if isinstance(value, str) else value
            habit.target_count = value

            # Eğer hedef değiştiyse
            if value != original_target_count:
                if value > original_target_count:
                    # Eğer yeni hedefe ulaşılamıyorsa bugünkü completed sıfırlanmalı
                    if habit.count < value:
                        # Bugünü completed_dates'den çıkar
                        today_str = today.isoformat()  # Tarihi string formatına çevir
                        if today_str in habit.completion_dates:
                            habit.completion_dates.remove(today_str)  # Bugünü çıkar
                        # last_completed_date'yi güncelle
                        if habit.completion_dates:
                            habit.last_completed_date = max(habit.completion_dates)  # En son tamamlanma tarihini güncelle
                        else:
                            habit.last_completed_date = None  # Eğer tamamlanma tarihi yoksa None yap
                

                elif value < original_target_count:
                    # Yeni hedefe ulaşılıyorsa completed artırılmalı
                    if habit.count >= value:
                        today_str = today.isoformat()
                        if today_str not in habit.completion_dates:  # 'in' kullanarak kontrol et
                            habit.completion_dates.append(today_str)  # 'push' yerine 'append' kullan
                            habit.last_completed_date = today  # last_completed_date'yi güncelle
            else :
                if habit.count < value:
                        # Bugünü completed_dates'den çıkar
                        today_str = today.isoformat()  # Tarihi string formatına çevir
                        if today_str in habit.completion_dates:
                            habit.completion_dates.remove(today_str)  # Bugünü çıkar
                        # last_completed_date'yi güncelle
                        if habit.completion_dates:
                            habit.last_completed_date = max(habit.completion_dates)  # En son tamamlanma tarihini güncelle
                        else:
                            habit.last_completed_date = None  # Eğer tamamlanma tarihi yoksa None yap
                if habit.count >= value:
                        today_str = today.isoformat()
                        if today_str not in habit.completion_dates:
                            print("habit.count >= value COMPLETION DATES GUNCELLEMESI")  # 'in' kullanarak kontrol et
                            habit.completion_dates.append(today_str)  # 'push' yerine 'append' kullan
                            habit.last_completed_date = today  # last_completed_date'yi güncelle
        habit.save()
        
        
        
        

    # Değişiklikleri kaydet ve streak güncelle
    print(habit.streak)
    habit.streak = habit.calculate_streak()
    print(habit.streak)

    print(habit.completed_count)
    habit.completed_count = habit.calculate_completed_count()
    print(habit.completed_count)
    

    print("habit saved")
    habit.save()

    # JSON serileştirme için tarihleri string formatına çevir
    response_data = {
        'message': 'Habit updated successfully!',
        'streak': habit.streak,
        'completed_count': habit.completed_count,
        'last_completed_date': habit.last_completed_date.isoformat() if isinstance(habit.last_completed_date, date) else habit.last_completed_date,  # String formatında döndür
    }

    print(habit.streak)
    return Response(response_data)






# 4. API: Bir alışkanlığı sil
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return Response({'message': 'Habit deleted successfully!'})





def add_habit_view(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'Alışkanlık başarıyla eklendi.')  # Başarı mesajı
            return render(request, 'habit_tracker/add_habit.html', {'form': form})# Başka bir view'a yönlendirin
        else:
            print(form.errors)  # Hataları kontrol et
    else:
        form = HabitForm()
    
    return render(request, 'habit_tracker/add_habit.html', {'form': form})

def increment_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.count += 1  # Sayıyı artır
    habit.save()
    return redirect('home')  # Ana sayfaya yönlendir
