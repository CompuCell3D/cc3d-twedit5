#include <cc3d/kernel.h>

#include <iostream>

namespace {

void start(CC3DKernelContext *ctx, void *state) {
    (void)ctx;
    (void)state;
}

void step(CC3DKernelContext *ctx, void *state) {
    (void)state;

    if (!ctx) {
        return;
    }

    for (auto cell : ctx->cells) {
        std::cerr << "MCS=" << ctx->mcs
                  << " cell id=" << static_cast<long>(cell.id)
                  << " type=" << static_cast<int>(static_cast<unsigned char>(cell.type))
                  << " volume=" << static_cast<long>(cell.volume)
                  << std::endl;
    }
}

void finish(CC3DKernelContext *ctx, void *state) {
    (void)ctx;
    (void)state;
}

} // namespace

extern "C" CC3D_STEPPABLE_EXPORT const CC3DSteppableV1 *cc3d_get_steppable_v1() {
    static const CC3DSteppableV1 api = {
        CC3D_KERNEL_ABI_VERSION,
        nullptr,
        &start,
        &step,
        &finish,
        nullptr,
    };
    return &api;
}
