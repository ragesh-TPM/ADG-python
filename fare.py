# this file is for managing the calculations and showig the main programming file clean without confusions

from routes import ROUTES, TRAIN_TYPES, CLASSES, PROMO_CODES

def calculate_slab_fare(distance):
    # first for Base slab fare calculation
    base_fare = 100
    
    if distance <= 100:
        slab_fare = distance * 1.0        # here 1.0 is multiplied because to make it float even the distance <= 100 instead of float()
    elif distance <= 300:
        slab_fare = 100 * 1.0 + (distance - 100) * 0.80
    else:
        slab_fare = 100 * 1.0 + 200 * 0.80 + (distance - 300) * 0.60
    
    return base_fare + slab_fare

def apply_senior_discount(slab_fare, age):
    # senior citizen discount
    if age > 60:
        return slab_fare * 0.60  # 40 pecent discount
    return slab_fare

def calculate_passenger_fare(distance, train_type, class_type, age, baggage):
    # complete fare calculation for one passenger
    # base slab fare
    slab_fare = calculate_slab_fare(distance)
    
    # senior discount
    discounted_fare = apply_senior_discount(slab_fare, age)
    
    # train premium
    train_premium = TRAIN_TYPES[train_type]["premium"]
    train_fare = discounted_fare * train_premium
    
    # class premium
    class_multiplier = CLASSES[class_type]["multiplier"]
    class_fare = train_fare * class_multiplier
    
    # excess baggage fee
    baggage_allowance = CLASSES[class_type]["baggage"]
    excess_baggage = max(0, baggage - baggage_allowance)
    baggage_fee = excess_baggage * 15
    total_with_baggage = class_fare + baggage_fee
    
    # flat surcharge
    surcharge = TRAIN_TYPES[train_type]["surcharge"]
    final_fare = total_with_baggage + surcharge
    
    return {
        "final_fare": round(final_fare, 2),
        "slab_fare": round(slab_fare, 2),
        "after_discount": round(discounted_fare, 2),
        "after_train": round(train_fare, 2),
        "after_class": round(class_fare, 2),
        "baggage_fee": round(baggage_fee, 2),
        "surcharge": surcharge,
        "excess_baggage": excess_baggage
    }

def apply_promo(subtotal, promo_code):
    # for applying promo code discount
    if promo_code not in PROMO_CODES:
        return subtotal, 0, "Invalid promo code - No discount applied"
    
    discount_value = PROMO_CODES[promo_code]
    if isinstance(discount_value, float):  # percentage discount
        discount_amount = subtotal * discount_value
    else:  # flat discount
        discount_amount = discount_value
    
    final_total = max(0, subtotal - discount_amount)
    return final_total, round(discount_amount, 2), f"Promo applied: {promo_code}"