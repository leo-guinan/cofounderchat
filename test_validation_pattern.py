"""
Test if model can learn Conscious Economics pattern from validation dataset.

This script:
1. Loads the validation dataset (20 examples)
2. Creates a tiny random model (or loads existing checkpoint)
3. Runs SFT for a few epochs
4. Checks if model starts emitting conscious economics blocks

Designed to run on MacBook (CPU or MPS) - no GPUs required.
"""

import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

import torch
from cofounderchat.common import get_base_dir, print0
from cofounderchat.gpt import GPT, GPTConfig
from cofounderchat.tokenizer import get_tokenizer
from tasks.conscious_validation import ConsciousValidation

def create_tiny_model(tokenizer):
    """Create a tiny random model for testing pattern learning"""
    config = GPTConfig(
        sequence_len=512,      # Short context for speed
        vocab_size=tokenizer.get_vocab_size(),
        n_layer=4,             # Tiny: 4 layers instead of 12
        n_head=4,              # Tiny: 4 heads instead of 12
        n_kv_head=4,
        n_embd=256,            # Tiny: 256 dim instead of 768
    )
    model = GPT(config)
    print0(f"Created tiny model: {sum(p.numel() for p in model.parameters())/1e6:.1f}M parameters")
    return model

def test_generation(model, tokenizer, prompt="Calculate LTV for $50/mo, 12 month retention, $200 CAC."):
    """Test if model generates conscious economics blocks"""
    print0("\n" + "="*60)
    print0("GENERATION TEST")
    print0("="*60)
    
    # Encode prompt
    bos = tokenizer.get_bos_token_id()
    user_start = tokenizer.encode_special("<|user_start|>")
    user_end = tokenizer.encode_special("<|user_end|>")
    assistant_start = tokenizer.encode_special("<|assistant_start|>")
    
    prompt_ids = [bos, user_start] + tokenizer.encode(prompt) + [user_end, assistant_start]
    
    # Generate
    model.eval()
    device = next(model.parameters()).device
    tokens = torch.tensor([prompt_ids], dtype=torch.long, device=device)
    
    with torch.no_grad():
        # Simple greedy generation (no KV cache for simplicity)
        generated = prompt_ids.copy()
        for _ in range(100):  # Generate up to 100 tokens
            logits = model.forward(tokens)
            next_token = logits[0, -1, :].argmax().item()
            generated.append(next_token)
            tokens = torch.tensor([generated], dtype=torch.long, device=device)
            
            # Stop at assistant_end
            if next_token == tokenizer.encode_special("<|assistant_end|>"):
                break
    
    # Decode and check for conscious economics blocks
    output = tokenizer.decode(generated)
    print0(f"\nPrompt: {prompt}")
    print0(f"\nGenerated ({len(generated)} tokens):")
    print0(output)
    
    # Check for conscious economics blocks
    blocks_found = []
    ce_blocks = ['<|assumptions|>', '<|risks|>', '<|tests|>', '<|metrics|>', 
                 '<|time_violence|>', '<|time_dividend|>', '<|compliance|>']
    for block in ce_blocks:
        if block in output:
            blocks_found.append(block)
    
    print0(f"\nConscious Economics blocks found: {len(blocks_found)}/{len(ce_blocks)}")
    if blocks_found:
        print0(f"  Blocks: {', '.join(blocks_found)}")
    else:
        print0(f"  (None yet - model hasn't learned pattern)")
    
    return len(blocks_found)

def run_validation_test(num_epochs=5, max_iterations=50):
    """Run SFT on validation dataset and test if pattern emerges"""
    
    print0("="*60)
    print0("CONSCIOUS ECONOMICS PATTERN VALIDATION TEST")
    print0("="*60)
    print0("\nThis test checks if a tiny model can learn to emit")
    print0("Conscious Economics blocks from 20 training examples.\n")
    
    # Setup
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print0(f"Device: {device}")
    
    # Load tokenizer
    print0("\n1. Loading tokenizer...")
    try:
        from cofounderchat.tokenizer import HuggingFaceTokenizer
        base_dir = os.path.expanduser("~/.cache/cofounderchat")
        tokenizer_dir = os.path.join(base_dir, "tokenizer")
        tokenizer = HuggingFaceTokenizer.from_directory(tokenizer_dir)
        print0(f"   ✓ Tokenizer loaded (vocab size: {tokenizer.get_vocab_size()})")
    except Exception as e:
        print0(f"   ✗ Could not load trained tokenizer: {e}")
        print0("   Need to train tokenizer first:")
        print0("   Run: python -m scripts.tok_train --vocab_size=8192")
        return
    
    # Load validation dataset
    print0("\n2. Loading validation dataset...")
    dataset = ConsciousValidation(split="train")
    print0(f"   ✓ Loaded {len(dataset)} examples")
    
    # Create tiny model
    print0("\n3. Creating tiny model...")
    model = create_tiny_model(tokenizer)
    model = model.to(device)
    print0(f"   ✓ Model on device: {device}")
    
    # Test generation BEFORE training
    print0("\n4. Testing generation BEFORE training...")
    blocks_before = test_generation(model, tokenizer)
    
    # Setup optimizer
    print0("\n5. Setting up training...")
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    
    # Training loop
    print0(f"\n6. Training ({num_epochs} epochs, max {max_iterations} iterations)...")
    print0("-"*60)
    
    pad_token_id = tokenizer.encode_special("<|assistant_end|>")
    model.train()
    
    iteration = 0
    for epoch in range(num_epochs):
        for i in range(len(dataset)):
            if iteration >= max_iterations:
                break
            
            # Get example
            ex = dataset[i % len(dataset)]
            ids, mask = tokenizer.render_conversation(ex)
            
            # Create input/target
            ids_tensor = torch.tensor(ids, dtype=torch.long, device=device)
            inputs = ids_tensor[:-1].unsqueeze(0)
            targets = ids_tensor[1:].unsqueeze(0).clone()
            
            # Mask targets where mask is 0
            mask_tensor = torch.tensor(mask[1:], dtype=torch.long, device=device)
            targets[0, mask_tensor == 0] = -1
            
            # Forward + backward
            loss = model(inputs, targets)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            
            iteration += 1
            
            # Log every 10 iterations
            if iteration % 10 == 0:
                print0(f"  Epoch {epoch+1}/{num_epochs}, Iter {iteration}/{max_iterations}, Loss: {loss.item():.4f}")
    
    print0(f"✓ Training complete ({iteration} iterations)")
    
    # Test generation AFTER training
    print0("\n7. Testing generation AFTER training...")
    blocks_after = test_generation(model, tokenizer)
    
    # Summary
    print0("\n" + "="*60)
    print0("RESULTS")
    print0("="*60)
    print0(f"Blocks before training: {blocks_before}")
    print0(f"Blocks after training:  {blocks_after}")
    
    if blocks_after > blocks_before:
        print0(f"\n✅ SUCCESS! Model learned to emit {blocks_after - blocks_before} new block(s)")
        print0("\nThis proves the Conscious Economics pattern is learnable!")
        print0("Next step: Train full model on cloud (8xH100, $96) and scale dataset.")
    elif blocks_after > 0:
        print0(f"\n⚠️  PARTIAL: Model emits some blocks but didn't improve from training")
        print0("May need more iterations or better initialization.")
    else:
        print0(f"\n❌ NOT LEARNED: Model doesn't emit conscious economics blocks yet")
        print0("\nPossible issues:")
        print0("  1. Need more training iterations (try --max_iterations=200)")
        print0("  2. Model too tiny (this is just a test, real model will work better)")
        print0("  3. Schema too complex (might need to simplify examples)")
        print0("\nBut don't worry - this is a TINY model. Real models learn better.")
    
    print0("\n" + "="*60)
    print0("NEXT STEPS")
    print0("="*60)
    
    if blocks_after > 0:
        print0("\n1. Pattern is learnable! Scale up:")
        print0("   - Rent Lambda Labs 8xH100 ($24/hr)")
        print0("   - Run: bash speedrun.sh (4 hours, $96)")
        print0("   - Generate 100K+ training examples")
        print0("   - Full conscious economics training pipeline")
    else:
        print0("\n1. Pattern not learned on tiny model. Options:")
        print0("   - Try more iterations: python test_validation_pattern.py --max_iterations=200")
        print0("   - Test on larger model (requires more memory)")
        print0("   - Or skip to cloud training anyway (real model learns better)")
    
    return blocks_after > blocks_before


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_epochs", type=int, default=5, help="Number of epochs")
    parser.add_argument("--max_iterations", type=int, default=50, help="Max training iterations")
    args = parser.parse_args()
    
    success = run_validation_test(num_epochs=args.num_epochs, max_iterations=args.max_iterations)
    
    exit(0 if success else 1)

